from rest_framework import serializers
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
        fields = '__all__'

    def validate(self, data):
        user = data['user']
        company = data['company']
        rules = Rule.objects.all()
        context = {
            'age': user.age,
            'country': user.country,
            'industry': company.industry,
            'location': company.location,
        }

        for rule in rules:
            if not rule.evaluate(context):
                raise serializers.ValidationError(f"Contract cannot be created: Rule {rule} not satisfied.")

        return data

class RuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rule
        fields = '__all__'
