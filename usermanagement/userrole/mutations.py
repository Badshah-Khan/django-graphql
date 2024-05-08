from graphene import Mutation, Boolean, Field, Int, ObjectType
from .models import UserRole
from .types import RoleType, RoleInputType

class CreateRole(Mutation):
    class Arguments:
        input = RoleInputType(required = True)

    success = Boolean()

    def mutate(self, info, input):
        is_auth = info.context.is_auth
        if not is_auth:
            raise Exception("Unauthorized")
        
        user_obj = info.context.user[0]
        token_obj = info.context.user[1]
        organization = token_obj['data']['organization']
        
        if user_obj.is_superuser != True and user_obj.is_staff != True:
            raise Exception("Not Allowed")
        if organization is None:
            raise Exception("Not Allowed")
        if user_obj.is_active is not True:
            raise Exception("You can't perform this action!")
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
        is_auth = info.context.is_auth
        if not is_auth:
            raise Exception("Unauthorized")
        
        user_obj = info.context.user[0]
        token_obj = info.context.user[1]
        organization = token_obj['data']['organization']
        
        if user_obj.is_superuser != True and user_obj.is_staff != True:
            raise Exception("Not Allowed")
        if organization is None:
            raise Exception("Not Allowed")
        if user_obj.is_active is not True:
            raise Exception("You can't perform this action!")
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
        is_auth = info.context.is_auth
        if not is_auth:
            raise Exception("Unauthorized")
        
        user_obj = info.context.user[0]
        token_obj = info.context.user[1]
        organization = token_obj['data']['organization']
        
        if user_obj.is_superuser != True and user_obj.is_staff != True:
            raise Exception("Not Allowed")
        if organization is None:
            raise Exception("Not Allowed")
        if user_obj.is_active is not True:
            raise Exception("You can't perform this action!")
        role = UserRole.objects.get(pk=id)
        if role and role.role.organization_id != organization:
            raise Exception("You can't perform this action!")
        role.delete()
        return DeleteRole(success=True)
    
class RoleMutation(ObjectType):
    create_role = CreateRole.Field()
    update_role = UpdateRole.Field()
    delete_role = DeleteRole.Field()