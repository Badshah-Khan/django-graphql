from graphene import ObjectType, Field, Int
from graphene_django.filter import DjangoFilterConnectionField
from .models import Organization
from address.models import Address
from .types import OrganizationType, OrgAddressType
from django.db.models import F
from usermanagement.utils import system_user, super_authorization


class OrganizationQuery(ObjectType):
    organizations = DjangoFilterConnectionField(OrganizationType)
    org_address = Field(OrgAddressType, id=Int(required=True))

    def resolve_organizations(self, info, **kwargs):
        system_user(info)
        result = Organization.objects.all()
        result = result.annotate(org_id = F('id'))
        return result
    
    def resolve_org_address(self, info, id):
        super_authorization(info)
        try:
            organization = Organization.objects.get(pk = id)
        except Organization.DoesNotExist:
            raise Exception("Organization doesn't exist!")
        if organization is None:
            raise Exception('Something went wrong')
        try:
            address = Address.objects.get(organization = id)
        except Address.DoesNotExist:
            address = None
        return {
            'organization': organization,
            'address': address
        }