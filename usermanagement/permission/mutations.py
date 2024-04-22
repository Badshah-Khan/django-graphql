from graphene import Mutation, Boolean, Field, Int, ObjectType
from .models import Permission
from .types import PermissionType, PermissionInputType

class CreatePermission(Mutation):
    class Arguments:
        input = PermissionInputType(required = True)

    success = Boolean()
    permission = Field(PermissionType)

    def mutate(self, info, input):
        permission = Permission.objects.create(permission_name=input.permission_name, description=input.description)
        return CreatePermission(success=True, permission=permission)

class UpdatePermission(Mutation):
    class Arguments:
        permission_id = Int(required=True)
        input = PermissionInputType(required = True)

    success = Boolean()
    permission = Field(PermissionType)

    def mutate(self, info, permission_id, input):
        permission = Permission.objects.get(pk=permission_id)
        if input.permission_name:
            permission.permission_name = input.permission_name
        if input.description:
            permission.description = input.description
        
        permission.save()
        return UpdatePermission(success=True, permission = permission)
    
class DeletePermission(Mutation):
    class Arguments:
        permission_id = Int(required=True)

    success = Boolean()

    def mutate(self, info, permission_id):
        permission = Permission.objects.get(pk=permission_id)
        permission.delete()
        return DeletePermission(success=True)
    
class PermissionMutation(ObjectType):
    create_permission = CreatePermission.Field()
    update_permission = UpdatePermission.Field()
    delete_permission = DeletePermission.Field()