from graphene import Mutation, Boolean, Int, ObjectType
from .models import UserRole
from .types import RoleInputType
from usermanagement.utils import super_staff_authorization, organization_validation

class CreateRole(Mutation):
    class Arguments:
        input = RoleInputType(required = True)

    success = Boolean()

    def mutate(self, info, input):
        user_obj = super_staff_authorization(info)
        organization = organization_validation(info)
        if organization is None:
            raise Exception("Not Allowed")
        if user_obj.id == input.user:
            raise Exception("Not Allowed")
        try:
            role = UserRole.objects.get(user_id = input.user)
            role.role_id = input.role
            role.save()
        except UserRole.DoesNotExist:
            UserRole.objects.create(role_id = input.role, user_id = input.user)
        return CreateRole(success=True)

class UpdateRole(Mutation):
    class Arguments:
        id = Int(required=True)
        input = RoleInputType(required = True)

    success = Boolean()

    def mutate(self, info, id, input):
        super_staff_authorization(info)
        organization = organization_validation(info)
        if organization is None:
            raise Exception("Not Allowed")
        role = UserRole.objects.get(pk=id)
        if role and role.role.organization_id != organization:
            raise Exception("You can't perform this action!")
        if input.role:
            role.role_id = input.role
        if input.user:
            role.user_id = input.user
        role.save()
        return UpdateRole(success=True)
    
class DeleteRole(Mutation):
    class Arguments:
        id = Int(required=True)

    success = Boolean()

    def mutate(self, info, id):
        super_staff_authorization(info)
        organization = organization_validation(info)
        role = UserRole.objects.get(pk=id)
        if role and role.role.organization_id != organization:
            raise Exception("You can't perform this action!")
        role.delete()
        return DeleteRole(success=True)
    
class RoleMutation(ObjectType):
    create_role = CreateRole.Field()
    update_role = UpdateRole.Field()
    delete_role = DeleteRole.Field()