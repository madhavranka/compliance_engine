from rest_framework import viewsets, status
from rest_framework.response import Response

from .models import Company, Contract, User, Rule, RuleSet
from .serializers import CompanySerializer, ContractSerializer, RuleSerializer, RuleSetSerializer, RuleValidationSerializer, UserSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

class ContractViewSet(viewsets.ModelViewSet):
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer

    def create(self, request, *args, **kwargs):

        # If a custom rule set is passed, that could be used
        rule_set_id = request.data.get('rule_set_id')
        ruleStructure = None
        if rule_set_id is not None:
            # validate the rule to belong to the company
            ruleStructure = request.data['rule_structure'] = RuleSet.objects.get(id=rule_set_id).get_rules()
        serializer = RuleValidationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            company = serializer.validated_data['company']
            rule_set = serializer.validated_data['rules']

            # Create a new rule set for the company
            if ruleStructure is None:
                newRuleSet = RuleSet(
                    company=company,
                )
                newRuleSet.set_rules(request.data['rule_structure'])
                newRuleSet.save()
            context = {
                'age': user.age,
                'country': user.country,
                'industry': company.industry,
                'location': company.location,
            }

            start_date = request.data.get('start_date')
            end_date = request.data.get('end_date')

            if Contract.objects.filter(user=user, company=company, start_date=start_date, end_date=end_date).exists():
                return Response(
                    {"detail": "Contract cannot be created: User already has a contract with this company in the given time period."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            if rule_set.evaluate(context):
                contract = Contract.objects.create(
                    user=user,
                    company=company,
                    start_date=start_date,
                    end_date=end_date
                )
                return Response({"detail": "Contract is created successfully", "contract_id": contract.id}, status=status.HTTP_201_CREATED)
            else:
                return Response({"detail": "Contract cannot be created: Rules not satisfied."}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RuleViewSet(viewsets.ModelViewSet):
    queryset = Rule.objects.all()
    serializer_class = RuleSerializer

class RuleSetViewSet(viewsets.ModelViewSet):
    queryset = RuleSet.objects.all()
    serializer_class = RuleSetSerializer