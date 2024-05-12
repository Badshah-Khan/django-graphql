from graphene import ObjectType, List, JSONString, Int, String
from .models import Attendance
from .types import AttendanceUserType

class AttendanceQuery(ObjectType):
    attendances = List(AttendanceUserType, where = JSONString(), limit = Int(), offset = Int(), order = String())

    def resolve_attendances(self, info, where = None, limit = 100, offset = 0, order = None):
        is_auth = info.context.is_auth
        if not is_auth:
            raise Exception("Unauthorized")
        user_obj = info.context.user[0]
        if user_obj.is_superuser != True and user_obj.is_staff != True:
            raise Exception("Not Allowed")
        
        token_obj = info.context.user[1]
        user_org = token_obj['data']['organization']
        if user_org is None:
            raise Exception("You don't have organization. Please Create to access this")
        
        result = Attendance.objects.filter(organization = user_org)
        attendance = [{'attendance': item, 'organization': item.organization, 'user': item.user} for item in result]
        return attendance
