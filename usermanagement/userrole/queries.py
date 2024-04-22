from graphene import ObjectType
from graphene_django.filter import DjangoFilterConnectionField
from .models import UserRole
from .types import RoleType


class UserRoleQuery(ObjectType):
    roles = DjangoFilterConnectionField(RoleType)

    def resolve_roles(self, info, **kwargs):
        return UserRole.objects.all()
