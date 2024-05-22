from graphene import Mutation, String, Boolean, Int, ObjectType
from .models import Leave
from .types import LeaveInput
from django.db.models import Q
from usermanagement.utils import user_authentication, organization_validation, super_staff_authorization

class CreateLeave(Mutation):
    class Arguments:
        input = LeaveInput(required = True)
    success = Boolean()
    message = String()
    def mutate(self, info, input):
        user_obj = user_authentication(info)
        organization = input.get('organization')
        organization_validation(info, organization)
        del input['organization']
        diff = input.to_date - input.from_date
        leave = Leave.objects.filter(
            Q(user = user_obj.id) & 
            Q(organization = organization) & 
            (
                (Q(from_date__lte=input.to_date) & Q(to_date__gte=input.from_date))
            )
        )
        if leave.exists() == False:
            Leave.objects.create(**input, user_id = user_obj.id, organization_id = organization, num_of_days = diff.days + 1)
            message = "Created successfully!"
        else:
            message = "Already exist!"
        return CreateLeave(success=True, message = message)

class ApproveLeave(Mutation):
    class Arguments:
        leave_id = Int(required=True)
        status = String(required = True)

    success = Boolean()

    def mutate(self, info, leave_id, status):
        user_obj = super_staff_authorization(info)
        leave = Leave.objects.get(pk=leave_id)
        leave.status = status
        if status == 'approved':
            leave.is_approved = True
        leave.approved_by = user_obj.id
        leave.save()
        return ApproveLeave(success=True)
    
class DeleteLeave(Mutation):
    class Arguments:
        leave_id = Int(required=True)

    success = Boolean()

    def mutate(self, info, leave_id):
        super_staff_authorization(info)
        leave = Leave.objects.get(pk=leave_id)
        leave.delete()
        return DeleteLeave(success=True)
    
class LeaveMutation(ObjectType):
    create_leave = CreateLeave.Field()
    approve_leave = ApproveLeave.Field()
    delete_leave = DeleteLeave.Field()