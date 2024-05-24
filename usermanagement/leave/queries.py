from graphene import ObjectType, List, JSONString
from .models import Leave
from .types import LeaveType
from django.db.models import Q
from datetime import datetime, timedelta
from usermanagement.utils import user_authentication

class LeaveQuery(ObjectType):
    leaves = List(LeaveType, where = JSONString())

    def resolve_leaves(self, info, where):
        user_obj = user_authentication(info)
        filter = where.get('filter', None)

        today = datetime.now().date()
        if filter is not None:
            if filter == 'year':
                start = today.replace(month=1, day=1)
                end = today.replace(month=12, day=31)
            elif filter == 'week':
                start = today - timedelta(days=today.weekday())
                end = start + timedelta(days=6)
            elif filter == 'month':
                start = today.replace(day=1)
                if start.month == 12:
                    end = start.replace(day=31)
                else:
                    end = (start.replace(month=start.month + 1, day=1) - timedelta(days=1))
            leave = Leave.objects.filter(Q(user = user_obj.id) & Q(from_date__lte=end) & Q(to_date__gte=start) & Q(is_approved = True))
        return leave
