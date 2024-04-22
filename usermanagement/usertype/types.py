from .models import UserType
from graphene_django import DjangoObjectType
from graphene import relay, InputObjectType, Int, String

class UserRoleType(DjangoObjectType):
    class Meta:
        model = UserType
        fields = '__all__'
        filter_fields = {
            'role': ['exact', 'icontains'],
            'organization': ['exact']
        }
        interfaces = (relay.Node,)

class UserRoleInputType(InputObjectType):
    role = String(required = True)
    user = Int(required = True)