# contracts/management/commands/seed_data.py

from django.core.management.base import BaseCommand
from contracts.models import Rule, User, Company

class Command(BaseCommand):
    help = 'Seed the database with initial data for testing'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding data...')
        
        # Clear existing data
        User.objects.all().delete()
        Company.objects.all().delete()
        Rule.objects.all().delete()

        # Seed User data
        users = [
            {"name": "Alice", "age": 28, "country": "USA"},
            {"name": "Bob", "age": 35, "country": "UK"},
            {"name": "Charlie", "age": 22, "country": "India"},
            {"name": "David", "age": 40, "country": "Canada"},
            {"name": "Eve", "age": 30, "country": "Australia"},
        ]
        for user_data in users:
            User.objects.create(**user_data)

        # Seed Company data
        companies = [
            {"name": "Tech Corp", "industry": "Software", "location": "USA"},
            {"name": "Health Inc", "industry": "Healthcare", "location": "UK"},
            {"name": "Edu Labs", "industry": "Education", "location": "India"},
            {"name": "Agri Foods", "industry": "Agriculture", "location": "Canada"},
            {"name": "Fin Services", "industry": "Finance", "location": "Australia"},
        ]
        for company_data in companies:
            Company.objects.create(**company_data)

        rules = [
            {"field_name": "age", "operator": ">", "value": "25"},
            {"field_name": "country", "operator": "==", "value": "USA"},
            {"field_name": "industry", "operator": "!=", "value": "Finance"},
        ]
        for rule_data in rules:
            Rule.objects.create(**rule_data)

        self.stdout.write(self.style.SUCCESS('Data seeding completed successfully!'))
