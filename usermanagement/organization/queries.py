from graphene import ObjectType

from graphene_django.filter import DjangoFilterConnectionField
from .models import Organization
from .types import OrganizationType


class OrganizationQuery(ObjectType):
    organizations = DjangoFilterConnectionField(OrganizationType)

    def resolve_organizations(self, info, **kwargs):
        print("info", info)
        return Organization.objects.all()
