from graphene import Mutation, Boolean, Field, Int, ObjectType
from .models import UserType
from .types import UserRoleType, UserRoleInputType

class CreateUserType(Mutation):
    class Arguments:
        input = UserRoleInputType(required = True)

    success = Boolean()
    user_type = Field(UserRoleType)

    def mutate(self, info, input):
        user_type = UserType.objects.create(role=input.role, organization=input.organization)
        return CreateUserType(success=True, user_type=user_type)

class UpdateUserType(Mutation):
    class Arguments:
        user_type_id = Int(required=True)
        input = UserRoleInputType(required = True)

    success = Boolean()
    user_type = Field(UserRoleType)

    def mutate(self, info, user_type_id, input):
        user_type = UserType.objects.get(pk=user_type_id)
        if input.role:
            user_type.role = input.role
        if input.organization:
            user_type.organization = input.organization
        
        user_type.save()
        return UpdateUserType(success=True, user_type = user_type)
    
class DeleteUserType(Mutation):
    class Arguments:
        user_type_id = Int(required=True)

    success = Boolean()

    def mutate(self, info, user_type_id):
        user_type = UserType.objects.get(pk=user_type_id)
        user_type.delete()
        return DeleteUserType(success=True)
    
class UserTypeMutation(ObjectType):
    create_user_type = CreateUserType.Field()
    update_user_type = UpdateUserType.Field()
    delete_user_type = DeleteUserType.Field()