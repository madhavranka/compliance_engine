from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action

from .models import Company, Contract, User
from .serializers import CompanySerializer, ContractSerializer, RuleSerializer, UserSerializer
from .rules.base import Rule, RuleWithPlaceholder

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

class ContractViewSet(viewsets.ModelViewSet):
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer

    @action(detail=True, methods=['post'])
    def evaluate_rule(self, request, pk=None):
        contract = self.get_object()
        rule_data = request.data.get('rule')
        rule = RuleWithPlaceholder(**rule_data)
        context = {
            'age': contract.user.age,
            'country': contract.user.country,
            # Add more fields as needed
        }
        placeholder_values = request.data.get('placeholders', {})
        result = rule.evaluate(context, placeholder_values)
        return Response({'result': result})

from .models import Rule

class RuleViewSet(viewsets.ModelViewSet):
    queryset = Rule.objects.all()
    serializer_class = RuleSerializer
