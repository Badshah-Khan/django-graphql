from graphene import Mutation, Boolean, Field, Int, ObjectType
from .models import UserRole
from .types import RoleType, RoleInputType

class CreateRole(Mutation):
    class Arguments:
        input = RoleInputType(required = True)

    success = Boolean()
    role = Field(RoleType)

    def mutate(self, info, input):
        role = UserRole.objects.create(role=input.role, user=input.user)
        return CreateRole(success=True, role=role)

class UpdateRole(Mutation):
    class Arguments:
        role_id = Int(required=True)
        input = RoleInputType(required = True)

    success = Boolean()
    role = Field(RoleType)

    def mutate(self, info, role_id, input):
        role = UserRole.objects.get(pk=role_id)
        if input.role:
            role.role = input.role
        if input.user:
            role.user = input.user
        
        role.save()
        return UpdateRole(success=True, role = role)
    
class DeleteRole(Mutation):
    class Arguments:
        role_id = Int(required=True)

    success = Boolean()

    def mutate(self, info, role_id):
        role = UserRole.objects.get(pk=role_id)
        role.delete()
        return DeleteRole(success=True)
    
class RoleMutation(ObjectType):
    create_role = CreateRole.Field()
    update_role = UpdateRole.Field()
    delete_role = DeleteRole.Field()