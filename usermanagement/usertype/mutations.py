from graphene import Mutation, Boolean, Int, ObjectType
from .models import UserType
from .types import UserRoleInputType
from organization.models import Organization
from usermanagement.utils import super_staff_authorization, organization_validation

class CreateUserType(Mutation):
    class Arguments:
        input = UserRoleInputType(required = True)

    success = Boolean()

    def mutate(self, info, input):
        super_staff_authorization(info)
        organization = organization_validation(info)
        UserType.objects.create(role=input.role, organization=Organization.objects.get(pk = organization))
        return CreateUserType(success=True)

class UpdateUserType(Mutation):
    class Arguments:
        id = Int(required=True)
        input = UserRoleInputType(required = True)

    success = Boolean()

    def mutate(self, info, id, input):
        super_staff_authorization(info)
        organization = organization_validation(info)
        user_type = UserType.objects.get(pk=id)
        if organization != 1 and organization != user_type.organization.id:
            raise Exception("Not Permit!")
        if input.role:
            user_type.role = input.role
        user_type.save()
        return UpdateUserType(success=True)
    
class DeleteUserType(Mutation):
    class Arguments:
        id = Int(required=True)

    success = Boolean()

    def mutate(self, info, id):
        super_staff_authorization(info)
        organization = organization_validation(info)
        user_type = UserType.objects.get(pk=id)
        if user_type.organization.id != organization:
            raise Exception("You can't perform this action!")
        user_type.delete()
        return DeleteUserType(success=True)
    
class UserTypeMutation(ObjectType):
    create_user_type = CreateUserType.Field()
    update_user_type = UpdateUserType.Field()
    delete_user_type = DeleteUserType.Field()