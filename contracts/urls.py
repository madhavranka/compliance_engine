from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CompanyViewSet, ContractViewSet, RuleSetViewSet, RuleViewSet, UserViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'companies', CompanyViewSet)
router.register(r'contracts', ContractViewSet)
router.register(r'rules', RuleViewSet)
router.register(r'rule-sets', RuleSetViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
