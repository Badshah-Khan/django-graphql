from graphene import Mutation, Boolean, Int, ObjectType
from .models import Attendance
from .types import AttendanceInput, AttendanceUpdateInput
from usermanagement.utils import user_authentication, organization_validation, super_staff_authorization, super_authorization

class CreateAttendance(Mutation):
    class Arguments:
        input = AttendanceInput(required = True)

    success = Boolean()

    def mutate(self, info, input):
        user_obj = user_authentication(info)
        user_org = organization_validation(info, input.organization)
        try:
            attendance = Attendance.objects.get(
                user = user_obj.id, 
                organization = user_org, 
                date = input.date
            )
            if attendance is not None:
                attendance.out_time = input.current_time
                attendance.save()
        except Attendance.DoesNotExist:
            Attendance.objects.create(
                date = input.date, 
                in_time = input.current_time, 
                organization_id = user_org, 
                user_id = user_obj.id
            )
        return CreateAttendance(success=True)

class UpdateAttendance(Mutation):
    class Arguments:
        id = Int(required=True)
        input = AttendanceUpdateInput(required = True)

    success = Boolean()

    def mutate(self, info, id, input):
        super_staff_authorization(info)
        organization_validation(info, input.organization)
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
        super_authorization(info)
        user_org = organization_validation(info)
        attendance = Attendance.objects.get(pk=id, organization_id = user_org)
        attendance.delete()
        return DeleteAttendance(success=True)
    
class AttendanceMutation(ObjectType):
    create_attendance = CreateAttendance.Field()
    update_attendance = UpdateAttendance.Field()
    delete_attendance = DeleteAttendance.Field()