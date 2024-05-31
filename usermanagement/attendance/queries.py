from graphene import ObjectType, List, JSONString, Int
from .models import Attendance
from .types import AttendanceUserType, UserAttendanceType
from datetime import datetime, timedelta
from django.db.models import Q
from usermanagement.utils import organization_validation, user_authentication, super_staff_authorization

class AttendanceQuery(ObjectType):
    attendances = List(AttendanceUserType, where = JSONString(), limit = Int())
    user_attendance = List(UserAttendanceType, where = JSONString(), limit = Int())

    def resolve_attendances(self, info, where = None, limit = None):
        user_obj = user_authentication(info)
        user_org = organization_validation(info)
        if user_org is None:
            raise Exception("You don't have organization. Please Create to access this")

        result = Attendance.objects.filter(user_id = user_obj.id, organization = user_org)
        today = datetime.now().date()
        start_date = today.replace(day=1)
        end_date = start_date.replace(day=1, month=start_date.month % 12 + 1) - timedelta(days=1)
        if where is not None:
            filter = where.get('filter', None)
            if filter is not None:
                if filter == 'week':
                    start_date = today - timedelta(days=today.weekday())
                    end_date = start_date + timedelta(days=6)
                elif filter == 'year':
                    start_date = today.replace(month=1, day=1)
                    end_date = today.replace(month=12, day=31)
        result = result.filter(Q(date__gte=start_date) & Q(date__lte=end_date))
        result = result.order_by('-date')
        if limit is not None:
            result = result[:limit]
        attendance = [{'attendance': item, 'organization': item.organization, 'user': item.user} for item in result]
        return attendance

    def resolve_user_attendance(self, info, where, limit):
        print("info", info)
        super_staff_authorization(info)
        user_org = organization_validation(info)
        if user_org is None:
            raise Exception("You don't have organization. Please Create to access this")

        query = '''select u.id, u.id as user_id, u.first_name, u.last_name, count(distinct aa.id) as present, count(distinct ll.id) as "absent" from auth_user u 
                    left join userorganization_userorganization uu on uu.user_id = u.id
                    left join attendance_attendance aa on u.id = aa.user_id left join leave_leave ll on ll.user_id = u.id  and ll.is_approved = true
                    where uu.organization_id = %s and aa.date between %s and %s
                    group by u.id, ll.created_at'''
        parameters = [user_org]

        today = datetime.now().date()
        start_date = today.replace(day=1)
        end_date = start_date.replace(day=1, month=start_date.month % 12 + 1) - timedelta(days=1)
        filter = where.get('filter', None)
        if filter is not None:
            if filter == 'week':
                start_date = today - timedelta(days=today.weekday())
                end_date = start_date + timedelta(days=6)
            elif filter == 'year':
                start_date = today.replace(month=1, day=1)
                end_date = today.replace(month=12, day=31)
        parameters.extend([start_date, end_date])
        attendance = Attendance.objects.raw(query, parameters)
        return attendance
