from rest_framework import serializers

from contracts.rules.base import RuleSet
from .models import User, Company, Contract, Rule

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'

class ContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contract
        exclude = ["created","updated"]

class RuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rule
        fields = '__all__'

class RuleSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = RuleSet
        fields = '__all__'

class RuleValidationSerializer(serializers.Serializer):
    user = serializers.IntegerField()
    company = serializers.IntegerField()
    rule_structure = serializers.ListField(
        allow_empty=False
    )

    def validate(self, data):
        # Validate user and company existence
        try:
            data['user'] = User.objects.get(pk=data['user'])
        except User.DoesNotExist:
            raise serializers.ValidationError("User does not exist.")

        try:
            data['company'] = Company.objects.get(pk=data['company'])
        except Company.DoesNotExist:
            raise serializers.ValidationError("Company does not exist.")
        # Validate rules existence
        data['rules'] = self._parse_rule_structure(data['rule_structure'])
        return data
    
    def _parse_rule_structure(self, structure):
        if isinstance(structure, int):
            try:
                return Rule.objects.get(pk=structure)
            except Rule.DoesNotExist:
                raise serializers.ValidationError(f"Rule with Id {structure} does not exist.")
        elif isinstance(structure, list):
            if not structure:
                raise serializers.ValidationError("Rule structure cannot be empty list.")
            logic = "AND" if isinstance(structure[0], int) else "OR"
            return RuleSet([self._parse_rule_structure(sub) for sub in structure], logic=logic)
        else:
            raise serializers.ValidationError("Invalid rule structure format.")