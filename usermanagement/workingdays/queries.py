from graphene import ObjectType, Int, String, List, JSONString
from .models import WorkingDays

class WorkingDaysType(ObjectType):
    total_working_days = Int()
    saturday = Int()
    sunday = Int()
    month = String()
    total_days = Int()
    year = String()

class WorkingDaysQuery(ObjectType):
    working_days = List(WorkingDaysType, where = JSONString(), limit = Int(), offset = Int(), order = String())

    def resolve_working_days(self, info, where = None, limit = 100, offset = 0, order = None):
        is_auth = info.context.is_auth
        if not is_auth:
            raise Exception("Unauthorized")
        
        user_obj = info.context.user[0]

        result = WorkingDays.objects.all()
        if where is not None:
            year = where.get('year', None)
            month = where.get('month', None)
            id = where.get('id', None)
            if year is not None:
                result = result.filter(year = year)
            if month is not None:
                result = result.filter(month = month)
            if id is not None:
                result = result.filter(pk= id)
        return result