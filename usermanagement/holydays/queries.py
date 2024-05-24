from graphene import List, Field, ObjectType, JSONString
from .types import HolydayType
from .models import Holydays
from django.db.models import Q
from datetime import datetime, timedelta
from usermanagement.utils import user_authentication

class HolydayQuery(ObjectType):
    holydays = List(HolydayType, where = JSONString())
    holyday = Field(HolydayType, where = JSONString())

    def resolve_holydays(self, info, where = {}):
        user_authentication(info)
        today = datetime.now().date()
        start_of_year = today.replace(month=1, day=1)
        end_of_year = today.replace(month=12, day=31)
        result = Holydays.objects.filter(Q(from_date__gte = start_of_year) & Q(from_date__gte=end_of_year))

        filter = where.get('filter', None)
        if filter is not None:
            if filter == 'month':
                start_of_month = today.replace(day=1)
                end_of_month = start_of_month.replace(day=1, month=start_of_month.month % 12 + 1) - timedelta(days=1)
                result = Holydays.objects.filter(Q(from_date__gte = start_of_month) & Q(from_date__gte=end_of_month))
            elif filter == 'week':
                start_of_week = today - timedelta(days=today.weekday())
                end_of_week = start_of_week + timedelta(days=6)
                result = Holydays.objects.filter(Q(from_date__gte = start_of_week) & Q(from_date__gte=end_of_week))
        return result