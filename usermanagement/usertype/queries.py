from graphene import ObjectType
from graphene_django.filter import DjangoFilterConnectionField
from .models import UserType
from .types import UserRoleType


class UserTypeQuery(ObjectType):
    user_types = DjangoFilterConnectionField(UserRoleType)

    def resolve_user_types(self, info, **kwargs):
        return UserType.objects.all()
