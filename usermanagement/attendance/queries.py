from graphene import ObjectType, List, JSONString, Int, String
from .models import Attendance
from .types import AttendanceUserType
from datetime import datetime, timedelta
from django.db.models import Q

class AttendanceQuery(ObjectType):
    attendances = List(AttendanceUserType, where = JSONString(), limit = Int(), offset = Int(), order = String())

    def resolve_attendances(self, info, where = None, limit = 100, offset = 0, order = None):
        is_auth = info.context.is_auth
        if not is_auth:
            raise Exception("Unauthorized")
        user_obj = info.context.user[0]
        
        token_obj = info.context.user[1]
        user_org = token_obj['data']['organization']
        if user_org is None:
            raise Exception("You don't have organization. Please Create to access this")
        
        result = Attendance.objects.filter(organization = user_org)
        if user_obj.is_superuser != True:
            result = result.filter(user_id = user_obj.id)
        if where is not None:
            filter = where.get('filter', None)
            if filter is not None:
                today = datetime.now().date()
                if filter == 'week':
                    start_of_week = today - timedelta(days=today.weekday())
                    end_of_week = start_of_week + timedelta(days=6)
                    result = result.filter(Q(date__gte=start_of_week) &
                        Q(date__lte=end_of_week))
                elif filter == 'month':
                    start_of_month = today.replace(day=1)
                    end_of_month = start_of_month.replace(day=1, month=start_of_month.month % 12 + 1) - timedelta(days=1)
                    result = result.filter(Q(date__gte=start_of_month) &
                        Q(date__lte=end_of_month))
                else:
                    start_of_year = today.replace(month=1, day=1)
                    end_of_year = today.replace(month=12, day=31)
                    result = result.filter(Q(date__gte=start_of_year) &
                        Q(date__lte=end_of_year))
        attendance = [{'attendance': item, 'organization': item.organization, 'user': item.user} for item in result]
        return attendance
