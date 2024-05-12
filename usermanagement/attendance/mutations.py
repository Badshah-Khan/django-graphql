from graphene import Mutation, Boolean, Field, Int, Date, Time, ObjectType
from .models import Attendance
from .types import AttendanceType, AttendanceInput, AttendanceUpdateInput

class CreateAttendance(Mutation):
    class Arguments:
        input = AttendanceInput(required = True)

    success = Boolean()

    def mutate(self, info, input):
        print("input", input)
        is_auth = info.context.is_auth
        if not is_auth:
            raise Exception("Unauthorized")
        user_obj = info.context.user[0]
        token_obj = info.context.user[1]
        user_org = token_obj['data']['organization']
        if user_org != input.organization:
            raise Exception("Invalid Organization!")
        try:
            attendance = Attendance.objects.get(user = user_obj.id, organization = user_org, date = input.date)
            if attendance is not None:
                attendance.out_time = input.current_time
                attendance.save()
        except Attendance.DoesNotExist:
            Attendance.objects.create(date = input.date, in_time = input.current_time, organization_id = user_org, user_id = user_obj.id)
        return CreateAttendance(success=True)

class UpdateAttendance(Mutation):
    class Arguments:
        id = Int(required=True)
        input = AttendanceUpdateInput(required = True)

    success = Boolean()

    def mutate(self, info, id, input):
        is_auth = info.context.is_auth
        if not is_auth:
            raise Exception("Unauthorized")
        user_obj = info.context.user[0]
        token_obj = info.context.user[1]
        user_org = token_obj['data']['organization']
        if user_obj.is_superuser != True and user_obj.is_staff != True:
            raise Exception("Not Allowed")
        if user_org != input.organization:
            raise Exception("Not Allowed")
        attendance = Attendance.objects.get(pk=id, user = input.user, organization = input.organization)
        date = input.get('date', None)
        if date is not None:
            attendance.date = date
        if input.in_time:
            attendance.in_time = input.in_time
        if input.out_time:
            attendance.out_time = input.out_time
        attendance.save()
        return UpdateAttendance(success=True)
    
class DeleteAttendance(Mutation):
    class Arguments:
        id = Int(required=True)

    success = Boolean()

    def mutate(self, info, id):
        is_auth = info.context.is_auth
        if not is_auth:
            raise Exception("Unauthorized")
        user_obj = info.context.user[0]
        token_obj = info.context.user[1]
        user_org = token_obj['data']['organization']
        if user_obj.is_superuser != True and user_obj.is_staff != True:
            raise Exception("Not Allowed")
        attendance = Attendance.objects.get(pk=id, organization_id = user_org)
        attendance.delete()
        return DeleteAttendance(success=True)
    
class AttendanceMutation(ObjectType):
    create_attendance = CreateAttendance.Field()
    update_attendance = UpdateAttendance.Field()
    delete_attendance = DeleteAttendance.Field()