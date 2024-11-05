from django.db import models
import json

class User(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    country = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

class Company(models.Model):
    name = models.CharField(max_length=100)
    industry = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class Contract(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class Rule(models.Model):
    field_name = models.CharField(max_length=100)
    operator = models.CharField(max_length=10)  # e.g., '==', '!=', '>', '<'
    value = models.CharField(max_length=100)  # This can contain placeholders
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, blank=True, related_name='rules')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

class RuleSet(models.Model):
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, blank=True, related_name='rule_set')
    name = models.CharField(max_length=100)
    rules = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    def set_rules(self, data):
        self.rules = json.dumps(data)
    def get_rules(self):
        return json.loads(self.rules)


