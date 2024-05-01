from .models import Organization
from graphene_django import DjangoObjectType
from graphene import relay, InputObjectType, String, Int, ObjectType, Field
from address.types import AddressType

class OrganizationType(DjangoObjectType):
    org_id = Int()
    class Meta:
        model = Organization
        fields = ('id', 'name', 'org_email', 'org_phone', 'logo', 'qr_code', 'slug', 'org_id')
        filter_fields = {
            'id': ['exact'],
            'name': ['exact', 'icontains'],
            'org_email': ['exact'],
            'org_phone': ['exact'],
        }
        interfaces = (relay.Node,)

class OrganizationInputType(InputObjectType):
    name = String(required = True)
    org_email = String(required = True)
    org_phone = String(required = True)
    slug = String(required = True)
    logo = String(required = True)

class AddressInputType(InputObjectType):
    street = String(required = True)
    city = String(required = True)
    state = String(required = True)
    postal_code = String(required = True)
    country = String(required = True)
    lat = String(required = True)
    long = String(required = True)

class OrganizationUpdateInputType(InputObjectType):
    name = String(required = True)
    org_email = String()
    org_phone = String()
    slug = String()
    logo = String()

class OrgAddressType(ObjectType):
    organization = Field(OrganizationType)
    address = Field(AddressType)

class OrganizationAddressType(ObjectType):
    name = String()
    org_email = String()
    org_phone = String()
    slug = String()
    logo = String()
    qr_code = String()