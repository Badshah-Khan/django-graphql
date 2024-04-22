from graphene import Mutation, Boolean, Field, Int, Date, Time, ObjectType
from .models import Attendance
from .types import AttendanceType

class CreateAttendance(Mutation):
    class Arguments:
        date = Date(required = True)
        in_time = Time(required = True)
        out_time = Time(required = True)
        user = Int(required = True)
        organization = Int(required = True)
    success = Boolean()
    attendance = Field(AttendanceType)

    def mutate(self, info, date, in_time, out_time, user, organization):
        attendance = Attendance.objects.create(date=date, in_time=in_time, out_time=out_time, user=user, organization=organization)
        return CreateAttendance(success=True, attendance=attendance)

class UpdateAttendance(Mutation):
    class Arguments:
        attendance_id = Int(required=True)
        date = Date()
        in_time = Time()
        out_time = Time()
        user = Int()
        organization = Int()

    success = Boolean()
    attendance = Field(AttendanceType)

    def mutate(self, info, attendance_id, date=None, in_time=None, out_time=None, user=None, organization=None):
        attendance = Attendance.objects.get(pk=attendance_id)
        if date:
            attendance.date = date
        if in_time:
            attendance.in_time = in_time
        if out_time:
            attendance.out_time = out_time
        if user:
            attendance.user = user
        if organization:
            attendance.organization = organization

        attendance.save()
        return UpdateAttendance(success=True, attendance = attendance)
    
class DeleteAttendance(Mutation):
    class Arguments:
        attendance_id = Int(required=True)

    success = Boolean()

    def mutate(self, info, attendance_id):
        attendance = Attendance.objects.get(pk=attendance_id)
        attendance.delete()
        return DeleteAttendance(success=True)
    
class AttendanceMutation(ObjectType):
    create_attendance = CreateAttendance.Field()
    update_attendance = UpdateAttendance.Field()
    delete_attendance = DeleteAttendance.Field()