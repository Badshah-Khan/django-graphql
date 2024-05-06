from .models import EmployeeAddress
from graphene_django import DjangoObjectType
from graphene import String

class EmpAddressType(DjangoObjectType):
    organization = String()
    first_name = String()
    last_name = String()
    class Meta:
        model = EmployeeAddress
        fields = '__all__'
