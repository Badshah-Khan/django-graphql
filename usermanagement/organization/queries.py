from graphene import ObjectType, Field, Int
from graphene_django.filter import DjangoFilterConnectionField
from .models import Organization
from address.models import Address
from .types import OrganizationType, OrgAddressType
from django.db.models import F


class OrganizationQuery(ObjectType):
    organizations = DjangoFilterConnectionField(OrganizationType)
    org_address = Field(OrgAddressType, id=Int(required=True))

    def resolve_organizations(self, info, **kwargs):
        is_auth = info.context.is_auth
        if not is_auth:
            raise Exception("Unauthorized")
        user_obj = info.context.user[0]
        if user_obj.is_superuser != True:
            raise Exception("Not Allowed")
        
        token_obj = info.context.user[1]
        user_org = token_obj['data']['organization']
        if user_org is None:
            raise Exception("You don't have organization. Please Create to access this")
        if user_org != 1:
            raise Exception("Not Permit!")
        result = Organization.objects.all()
        result = result.annotate(org_id = F('id'))
        return result
    
    def resolve_org_address(self, info, id):
        is_auth = info.context.is_auth
        if not is_auth:
            raise Exception("Unauthorized")
        user_obj = info.context.user[0]
        if user_obj.is_superuser != True:
            raise Exception("Not Allowed")
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