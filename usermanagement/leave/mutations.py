from graphene import Mutation, String, Boolean, Field, Int, Date, Time, ObjectType
from .models import Leave
from .types import LeaveType

class CreateLeave(Mutation):
    class Arguments:
        leave_type = String(required = True)
        reason = String()
        start_date = Date(required = True)
        to_date = Date(required = True)
        user = Int(required = True)
        organization = Int(required = True)
    success = Boolean()
    leave = Field(LeaveType)

    def mutate(self, info, leave_type, start_date, to_date, user, organization, reason = None):
        leave = Leave.objects.create(leave_type=leave_type, reason=reason, from_date=start_date, to_date=to_date, user=user, organization=organization)
        return CreateLeave(success=True, leave=leave)

class UpdateLeave(Mutation):
    class Arguments:
        leave_id = Int(required=True)
        leave_type = String()
        reason = String()
        start_date = Date()
        to_date = Date()
        user = Int()
        organization = Int()
        approved_by = Int()

    success = Boolean()
    leave = Field(LeaveType)

    def mutate(self, info, leave_id, leave_type=None, reason=None, start_date=None, to_date=None, approved_by = None, user=None, organization=None):
        leave = Leave.objects.get(pk=leave_id)
        if leave_type:
            leave.leave_type = leave_type
        if reason:
            leave.reason = reason
        if start_date:
            leave.from_date = start_date
        if to_date:
            leave.to_date = to_date
        if approved_by:
            leave.approved_by = approved_by
            leave.is_approved = True
        if user:
            leave.user = user
        if organization:
            leave.organization = organization

        leave.save()
        return UpdateLeave(success=True, leave = leave)
    
class DeleteLeave(Mutation):
    class Arguments:
        leave_id = Int(required=True)

    success = Boolean()

    def mutate(self, info, leave_id):
        leave = Leave.objects.get(pk=leave_id)
        leave.delete()
        return DeleteLeave(success=True)
    
class LeaveMutation(ObjectType):
    create_leave = CreateLeave.Field()
    update_leave = UpdateLeave.Field()
    delete_leave = DeleteLeave.Field()