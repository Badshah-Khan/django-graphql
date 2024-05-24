from graphene import ObjectType, Int, String, Field, JSONString
from .models import WorkingDays
from configuration.models import Configuration
from holydays.models import Holydays
from django.db.models import Q
from datetime import datetime, timedelta
from usermanagement.utils import organization_validation, user_authentication

class WorkingDaysType(ObjectType):
    total_working_days = Int()
    saturday = Int()
    sunday = Int()
    month = String()
    total_days = Int()
    year = String()

class WorkingDaysQuery(ObjectType):
    working_days = Field(WorkingDaysType, where = JSONString())

    def resolve_working_days(self, info, where = {}):
        user_authentication(info)
        user_org = organization_validation(info)
        year = where.get('year', None)
        month = where.get('month', None)
        try:
            config = Configuration.objects.get(organization_id = user_org)
            saturday_working = config.configuration
        except Configuration.DoesNotExist:
            saturday_working = {
                'isSaturdayWorking': False
            }

        today = datetime.now().date()
        filter = where.get('filter', None)
        working_days = 0
        if filter is not None:
            if filter == 'year':
                result = WorkingDays.objects.filter(year = year)
                for item in result:
                    if saturday_working['isSaturdayWorking'] == True:
                        working_days += item.total_working_days + item.saturday
                    else:
                        working_days += item.total_working_days
                start = today.replace(month=1, day=1)
                end = today.replace(month=12, day=31)
            elif filter == 'week':
                working_days += 5
                start = today - timedelta(days=today.weekday())
                end = start + timedelta(days=6)
            elif filter == 'month':
                result = WorkingDays.objects.get(year = year, month=month)
                if saturday_working['isSaturdayWorking'] == True:
                        working_days += result.total_working_days + result.saturday
                else:
                    working_days += result.total_working_days
                start = today.replace(day=1)
                end = start.replace(day=1, month=start.month % 12 + 1) - timedelta(days=1)
            holydays = Holydays.objects.filter(Q(from_date__gte = start) & Q(from_date__lte=end))
        holyday = 0
        for item in holydays:
            holyday += item.num_of_days
        total_working_days = working_days - holyday
        return {
            'total_working_days': total_working_days,
        }