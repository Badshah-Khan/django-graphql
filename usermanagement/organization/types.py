from .models import Organization
from graphene_django import DjangoObjectType
from graphene import relay, InputObjectType, String, Int

class OrganizationType(DjangoObjectType):
    org_id = Int()
    class Meta:
        model = Organization
        fields = ('id', 'name', 'org_email', 'org_phone', 'logo', 'qr_code', 'org_id')
        filter_fields = {
            'id': ['exact'],
            'name': ['exact', 'icontains'],
            'org_email': ['exact'],
            'org_phone': ['exact'],
        }
        interfaces = (relay.Node,)

class OrganizationInputType(InputObjectType):
    name = String(required = True)
    org_email = String()
    org_phone = String()