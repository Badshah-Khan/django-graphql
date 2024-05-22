from graphene import ObjectType, JSONString, Field, String, DateTime, Boolean, Int
from .models import UserStatus
from employeedetails.models import Employee

class UserStatusType(ObjectType):
    first_name = String()
    last_name = String()
    profile = String()
    last_seen = DateTime()
    is_online = Boolean()
    user_id = Int()

class UserStatusQuery(ObjectType):
    user_status = Field(UserStatusType, where = JSONString())

    def resolve_user_status(self, info, where):
        is_auth = info.context.is_auth
        if not is_auth:
            raise Exception("Unauthorized")
        
        user_id = where.get('user_id', None)
        if user_id is None:
            raise Exception('Missing User Id')
        result = UserStatus.objects.get(user_id = user_id)
        profile = Employee.objects.get(user_id = user_id)

        return {
            'first_name': result.user.first_name,
            'last_name': result.user.last_name,
            'is_online': result.is_online,
            'last_seen': result.last_seen,
            'profile': profile.profile,
            'user_id': user_id
        }