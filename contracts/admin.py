from django.contrib import admin
from .models import RuleSet, User, Company, Contract, Rule

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'age', 'country')

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'industry', 'location')

@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'company', 'start_date', 'end_date')

@admin.register(Rule)
class RuleAdmin(admin.ModelAdmin):
    list_display = ('id', 'field_name', 'operator', 'value')

@admin.register(RuleSet)
class RuleSetAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'company', 'rules')

