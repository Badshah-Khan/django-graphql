from graphene import ObjectType, List, JSONString, Int, String
from .models import UserType
from .types import UserRoleType
from usermanagement.utils import super_staff_authorization, organization_validation


class UserTypeQuery(ObjectType):
    user_types = List(UserRoleType, where = JSONString(), limit = Int(), offset = Int(), order = String())

    def resolve_user_types(self, info, where = None, limit = 100, offset = 0, order = ''):
        super_staff_authorization(info)
        organization = organization_validation(info)
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
