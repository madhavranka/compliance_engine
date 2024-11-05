from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CompanyViewSet, ContractViewSet, RuleViewSet, UserViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'companies', CompanyViewSet)
router.register(r'contracts', ContractViewSet)
router.register(r'rules', RuleViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
