from graphene import ObjectType

from graphene_django.filter import DjangoFilterConnectionField
from .models import Organization
from .types import OrganizationType
from django.db.models import F


class OrganizationQuery(ObjectType):
    organizations = DjangoFilterConnectionField(OrganizationType)

    def resolve_organizations(self, info, **kwargs):
        is_auth = info.context.is_auth
        if not is_auth:
            raise Exception("Unauthorized")
        user_obj = info.context.user[0]
        if user_obj.is_superuser != True:
            raise Exception("Not Allowed")
        result = Organization.objects.all()
        result = result.annotate(org_id = F('id'))
        for i in result:
            print(i.org_id)
        return result
