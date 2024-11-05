from django.test import TestCase

from .models import User, Company, Contract, Rule
from .rules.base import RuleEvaluator, RuleSet, RuleWithPlaceholder


class ComplianceEngineTests(TestCase):
    def test_user_creation(self):
        response = self.client.post('/api/users/', {'name': 'John Doe', 'age': 30, 'country': 'USA'})
        self.assertEqual(response.status_code, 201)


class RuleEvaluationTestCase(TestCase):

    def setUp(self):
        # Context for testing
        self.context = {
            'age': 30,
            'country': 'USA',
            'industry': 'Software',
            'location': 'USA'
        }

    def test_single_rule_evaluation(self):
        # Test a single rule evaluation
        rule = RuleEvaluator(field_name='age', operator='>', value=25)
        self.assertTrue(rule.evaluate(self.context))

        rule_fail = RuleEvaluator(field_name='age', operator='>', value=35)
        self.assertFalse(rule_fail.evaluate(self.context))

    def test_rule_set_with_and_logic(self):
        # Test RuleSet with AND logic
        rule1 = RuleEvaluator(field_name='age', operator='>', value=25)
        rule2 = RuleEvaluator(field_name='country', operator='==', value='USA')
        and_rule_set = RuleSet(rules=[rule1, rule2], logic='AND')
        self.assertTrue(and_rule_set.evaluate(self.context))

        # Test failing AND condition
        rule3 = RuleEvaluator(field_name='industry', operator='==', value='Finance')
        and_rule_set_fail = RuleSet(rules=[rule1, rule3], logic='AND')
        self.assertFalse(and_rule_set_fail.evaluate(self.context))

    def test_rule_set_with_or_logic(self):
        # Test RuleSet with OR logic
        rule1 = RuleEvaluator(field_name='age', operator='>', value=35)
        rule2 = RuleEvaluator(field_name='country', operator='==', value='USA')
        or_rule_set = RuleSet(rules=[rule1, rule2], logic='OR')
        self.assertTrue(or_rule_set.evaluate(self.context))

        # Test failing OR condition
        rule3 = RuleEvaluator(field_name='industry', operator='==', value='Finance')
        rule4 = RuleEvaluator(field_name='location', operator='==', value='Canada')
        or_rule_set_fail = RuleSet(rules=[rule3, rule4], logic='OR')
        self.assertFalse(or_rule_set_fail.evaluate(self.context))

    def test_nested_rule_set(self):
        # Test nested RuleSet evaluation
        rule1 = RuleEvaluator(field_name='age', operator='>', value=25)
        rule2 = RuleEvaluator(field_name='country', operator='==', value='USA')
        and_rule_set1 = RuleSet(rules=[rule1, rule2], logic='AND')

        rule3 = RuleEvaluator(field_name='industry', operator='!=', value='Finance')
        rule4 = RuleEvaluator(field_name='location', operator='==', value='USA')
        and_rule_set2 = RuleSet(rules=[rule3, rule4], logic='AND')

        complex_rule_set = RuleSet(rules=[and_rule_set1, and_rule_set2], logic='OR')
        self.assertTrue(complex_rule_set.evaluate(self.context))

        # Test nested RuleSet with failing condition
        rule5 = RuleEvaluator(field_name='age', operator='>', value=35)
        and_rule_set_fail = RuleSet(rules=[rule5, rule3], logic='AND')
        complex_rule_set_fail = RuleSet(rules=[and_rule_set_fail, and_rule_set2], logic='OR')
        self.assertTrue(complex_rule_set_fail.evaluate(self.context))

    def test_rule_with_placeholder(self):
        # Test RuleWithPlaceholder
        rule_with_placeholder = RuleWithPlaceholder(field_name='country', operator='==', value='{{country}}')
        placeholder_values = {'country': 'USA'}
        self.assertTrue(rule_with_placeholder.evaluate(self.context, placeholder_values))

        rule_with_placeholder_fail = RuleWithPlaceholder(field_name='age', operator='>', value='{{age}}')
        placeholder_values_fail = {'age': 35}
        self.assertFalse(rule_with_placeholder_fail.evaluate(self.context, placeholder_values_fail))


from rest_framework.test import APITestCase, APIClient
from rest_framework import status

class ContractAPITestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(name="John Doe", age=30, country="USA")
        self.company = Company.objects.create(name="Tech Corp", industry="Software", location="USA")

class EvaluateRuleTestCase(TestCase):

    def setUp(self):
        # Create test data
        self.client = APIClient()

        # Create users
        self.user1 = User.objects.create(name="Alice", age=30, country="USA")

        # Create companies
        self.company1 = Company.objects.create(name="Tech Corp", industry="Software", location="USA")

        # Create rules
        self.rule1 = Rule.objects.create(field_name='age', operator='>', value='25')
        self.rule2 = Rule.objects.create(field_name='country', operator='==', value='USA')
        self.rule3 = Rule.objects.create(field_name='industry', operator='!=', value='Finance')

    def test_contract_creation_success(self):
        # Test successful contract creation
        data = {
            "user": self.user1.id,
            "company": self.company1.id,
            "rule_structure": [[self.rule1.id, self.rule2.id], [self.rule3.id]],
            "start_date": "2023-01-01",
            "end_date": "2023-12-31"
        }
        response = self.client.post('/api/contracts/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('contract_id', response.data)

    def test_contract_creation_failure_due_to_rules(self):
        # Test contract creation failure due to unsatisfied rules
        # Modify rule so it fails
        self.rule1.value = '35'
        self.rule1.save()

        data = {
            "user": self.user1.id,
            "company": self.company1.id,
            "rule_structure": [[self.rule1.id, self.rule2.id]],
            "start_date": "2023-01-01",
            "end_date": "2023-12-31"
        }
        response = self.client.post('/api/contracts/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['detail'], "Contract cannot be created: Rules not satisfied.")

    def test_contract_creation_failure_due_to_existing_contract(self):
        # Test failure due to existing contract for the same user and company in the given time
        Contract.objects.create(
            user=self.user1,
            company=self.company1,
            start_date="2023-01-01",
            end_date="2023-12-31"
        )

        data = {
            "user": self.user1.id,
            "company": self.company1.id,
            "rule_structure": [[self.rule1.id, self.rule2.id], [self.rule3.id]],
            "start_date": "2023-01-01",
            "end_date": "2023-12-31"
        }
        response = self.client.post('/api/contracts/', data, format='json')
        # Assuming you add logic to prevent duplicate contracts
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['detail'], "Contract cannot be created: User already has a contract with this company in the given time period.")

