from .models import Organization
from graphene_django import DjangoObjectType
from graphene import relay, InputObjectType, String

class OrganizationType(DjangoObjectType):
    class Meta:
        model = Organization
        fields = '__all__'
        filter_fields = {
            'name': ['exact', 'icontains'],
            'org_email': ['exact'],
            'org_phone': ['exact'],
        }
        interfaces = (relay.Node,)

class OrganizationInputType(InputObjectType):
    name = String(required = True)
    org_email = String()
    org_phone = String()