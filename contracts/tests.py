from django.test import TestCase

from .models import User, Company, Contract
from .rules.base import Rule, RuleWithPlaceholder


class ComplianceEngineTests(TestCase):
    
    def test_user_creation(self):
        response = self.client.post('/api/users/', {'name': 'John Doe', 'age': 30, 'country': 'USA'})
        self.assertEqual(response.status_code, 201)


class RuleEvaluationTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(name="John Doe", age=30, country="USA")
        self.company = Company.objects.create(name="Tech Corp", industry="Software", location="USA")
        self.contract = Contract.objects.create(user=self.user, company=self.company, start_date="2022-01-01", end_date="2023-01-01")

    def test_rule_evaluation(self):
        rule = Rule(field_name="age", operator=">", value=25)
        context = {"age": self.user.age}
        self.assertTrue(rule.evaluate(context))

    def test_rule_with_placeholder(self):
        rule = RuleWithPlaceholder(field_name="country", operator="==", value="{{country}}")
        context = {"country": self.user.country}
        placeholder_values = {"country": "USA"}
        self.assertTrue(rule.evaluate(context, placeholder_values))


from rest_framework.test import APITestCase, APIClient
from rest_framework import status

class ContractAPITestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(name="John Doe", age=30, country="USA")
        self.company = Company.objects.create(name="Tech Corp", industry="Software", location="USA")

    def test_create_contract(self):
        data = {
            "user": self.user.id,
            "company": self.company.id,
            "start_date": "2023-01-01",
            "end_date": "2023-12-31"
        }
        response = self.client.post("/api/contracts/", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Contract.objects.count(), 1)
        self.assertEqual(Contract.objects.get().user, self.user)

    def test_evaluate_rule(self):
        contract = Contract.objects.create(user=self.user, company=self.company, start_date="2023-01-01", end_date="2023-12-31")
        rule_data = {
            "rule": {
                "field_name": "age",
                "operator": ">",
                "value": "25"
            },
            "placeholders": {}
        }
        response = self.client.post(f"/api/contracts/{contract.id}/evaluate_rule/", rule_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['result'])

