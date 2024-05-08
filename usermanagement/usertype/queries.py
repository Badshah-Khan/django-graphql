from graphene import ObjectType, List, JSONString, Int, String
from .models import UserType
from .types import UserRoleType


class UserTypeQuery(ObjectType):
    user_types = List(UserRoleType, where = JSONString(), limit = Int(), offset = Int(), order = String())

    def resolve_user_types(self, info, where = None, limit = 100, offset = 0, order = ''):
        is_auth = info.context.is_auth
        if not is_auth:
            raise Exception("Unauthorized")
        
        user_obj = info.context.user[0]
        token_obj = info.context.user[1]
        organization = token_obj['data']['organization']
        
        if user_obj.is_superuser != True and user_obj.is_staff != True:
            raise Exception("Not Allowed")
        if organization is None:
            raise Exception("Not Allowed")
        if user_obj.is_active is not True:
            raise Exception("You can't perform this action!")
        try:
            result = UserType.objects.all()
        except UserType.DoesNotExist:
            result =  []
        if where is not None and len(result) > 0:
            role_id = where.get('id', None)
            user_organization = where.get('organization', None)
            if user_organization is not None:
                result = result.filter(organization = user_organization)
            if role_id is not None:
                result = result.filter(id = role_id)
        result = result.filter(organization = organization)
        return result
