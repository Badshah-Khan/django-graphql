from .models import UserType
from graphene_django import DjangoObjectType
from graphene import relay, InputObjectType, Int, String

class UserRoleType(DjangoObjectType):
    class Meta:
        model = UserType
        fields = '__all__'

class UserRoleInputType(InputObjectType):
    role = String(required = True)
    user = Int()