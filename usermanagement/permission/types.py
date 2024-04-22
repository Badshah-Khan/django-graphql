from .models import Permission
from graphene_django import DjangoObjectType
from graphene import relay, InputObjectType, String

class PermissionType(DjangoObjectType):
    class Meta:
        model = Permission
        fields = '__all__'
        filter_fields = {
            'permission_name': ['exact', 'icontains'],
            'description': ['exact', 'icontains']
        }
        interfaces = (relay.Node,)

class PermissionInputType(InputObjectType):
    permission_name = String(required = True)
    description = String()