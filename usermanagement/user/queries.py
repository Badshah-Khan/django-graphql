from graphene import ObjectType, String, List
from userorganization.models import UserOrganization
from .types import UserType, ResolveUserType


class UserQuery(ObjectType):
    users = List(UserType, search = String())

    def resolve_users(self, info, search = None, **kwargs):
        if not info.context.user.is_authenticated:
            raise Exception("Unauthorized")
        user_obj = info.context.user[0]
        if user_obj.is_superuser != True:
            raise Exception("Not Allowed")
        user_organizations = UserOrganization.objects.select_related('user', 'organization').all()
        data = []
        for user_org in user_organizations:
            user = user_org.user
            organization = user_org.organization
            result = ResolveUserType(user, organization)
            data.append(result.format())
        return data
