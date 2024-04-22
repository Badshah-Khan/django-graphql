from .models import UserRole
from graphene_django import DjangoObjectType
from graphene import relay, InputObjectType, Int

class RoleType(DjangoObjectType):
    class Meta:
        model = UserRole
        fields = '__all__'
        filter_fields = {
            'role': ['exact'],
            'user': ['exact']
        }
        interfaces = (relay.Node,)

class RoleInputType(InputObjectType):
    role = Int(required = True)
    user = Int(required = True)