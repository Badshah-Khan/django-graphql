from graphene import Mutation, Boolean, Int, ObjectType
from .models import UserType
from .types import UserRoleInputType
from organization.models import Organization

class CreateUserType(Mutation):
    class Arguments:
        input = UserRoleInputType(required = True)

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
        UserType.objects.create(role=input.role, organization=Organization.objects.get(pk = organization))
        return CreateUserType(success=True)

class UpdateUserType(Mutation):
    class Arguments:
        id = Int(required=True)
        input = UserRoleInputType(required = True)

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
        user_type = UserType.objects.get(pk=id)
        if input.role:
            user_type.role = input.role
        user_type.save()
        return UpdateUserType(success=True)
    
class DeleteUserType(Mutation):
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
        user_type = UserType.objects.get(pk=id)
        if user_type.organization.id != organization:
            raise Exception("You can't perform this action!")
        user_type.delete()
        return DeleteUserType(success=True)
    
class UserTypeMutation(ObjectType):
    create_user_type = CreateUserType.Field()
    update_user_type = UpdateUserType.Field()
    delete_user_type = DeleteUserType.Field()