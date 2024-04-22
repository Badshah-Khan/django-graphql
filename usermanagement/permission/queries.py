from graphene import ObjectType
from graphene_django.filter import DjangoFilterConnectionField
from .models import Permission
from .types import PermissionType


class PermissionQuery(ObjectType):
    permissions = DjangoFilterConnectionField(PermissionType)

    def resolve_permissions(self, info, **kwargs):
        return Permission.objects.all()
