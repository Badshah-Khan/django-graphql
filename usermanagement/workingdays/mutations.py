from graphene import Mutation, Boolean, Int, ObjectType
from workingdays.models import WorkingDays
import calendar
from datetime import datetime
from holydays.models import Holydays
from .types import HolydaysInput

class CreateWorkingDays(Mutation):
    class Arguments:
        year = Int(required = True)

    success = Boolean()

    def mutate(self, info, year):
        is_auth = info.context.is_auth
        if not is_auth:
            raise Exception("Unauthorized")
        user_obj = info.context.user[0]
        if user_obj.is_superuser != True:
            raise Exception("Not Allowed")
        token_obj = info.context.user[1]
        user_org = token_obj['data']['organization']
        if user_org != 1:
            raise Exception("Not Allowed!")
        try:
            current_date = datetime.now().date()
            current_month = current_date.strftime("%B")
            WorkingDays.objects.get(year = year, month = current_month)
        except WorkingDays.DoesNotExist:
            for month in range(12):
                sat = 0
                sun = 0
                num_days_in_month = calendar.monthrange(year, month+1)[1]
                cal = calendar.monthcalendar(year, month + 1)

                for week in cal:
                    if week[calendar.SATURDAY] != 0:
                        sat += 1
                    if week[calendar.SUNDAY] != 0:
                        sun += 1
                twd = num_days_in_month - (sun + sat)
                WorkingDays.objects.create(
                    total_days = num_days_in_month, 
                    total_working_days = twd, 
                    sunday = sun, 
                    month = calendar.month_name[month + 1],
                    saturday = sat,
                    year = year
                )
        return CreateWorkingDays(success = True)

class CreateHolydays(Mutation):
    class Arguments:
        input = HolydaysInput(required = True)

    success = Boolean()

    def mutate(self, info, input):
        is_auth = info.context.is_auth
        if not is_auth:
            raise Exception("Unauthorized")
        user_obj = info.context.user[0]
        if user_obj.is_superuser != True and user_obj.is_staff != True:
            raise Exception("Not Allowed")
        token_obj = info.context.user[1]
        user_org = token_obj['data']['organization']
        if user_org != input.organization:
            raise Exception("Not Allowed!")
        Holydays.objects.create(**input)
        return CreateHolydays(success = True)

class WorkingDaysMutation(ObjectType):
    create_working_days = CreateWorkingDays.Field()
    create_holydays = CreateHolydays.Field()