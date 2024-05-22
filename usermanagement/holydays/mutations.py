from graphene import Mutation, ObjectType, Boolean, Int
from .types import HolydayInput
from .models import Holydays

class CreateHolyday(Mutation):
    class Arguments:
        input = HolydayInput(required = True)
    
    success = Boolean()

    def mutate(self, info, input):
        is_auth = info.context.is_auth
        if not is_auth:
            raise Exception("Unauthorized")
        user_obj = info.context.user[0]
        token_obj = info.context.user[1]
        user_org = token_obj['data']['organization']
        if user_obj.is_superuser != True and user_obj.is_staff != True:
            raise Exception("Not Allowed")
        organization = input.get('organization')
        if user_org != organization:
            raise Exception("Not Allowed")
        del input['organization']
        Holydays.objects.create(**input, organization_id = organization)

        return CreateHolyday(success = True)

class UpdateHolyday(Mutation):
    class Arguments:
        input = HolydayInput(required = True)
        id = Int(required = True)
    success = Boolean()

    def mutate(self, info, input, id):
        is_auth = info.context.is_auth
        if not is_auth:
            raise Exception("Unauthorized")
        user_obj = info.context.user[0]
        token_obj = info.context.user[1]
        user_org = token_obj['data']['organization']
        if user_obj.is_superuser != True and user_obj.is_staff != True:
            raise Exception("Not Allowed")
        organization = input.get('organization')
        if user_org != organization:
            raise Exception("Not Allowed")
        del input['organization']

        holyday = Holydays.objects.get(pk= id)

        return UpdateHolyday(success = True)

class DeleteHolyday(Mutation):
    class Arguments:
        id = Int(required = True)
    success = Boolean()

    def mutate(self, info, id):
        is_auth = info.context.is_auth
        if not is_auth:
            raise Exception("Unauthorized")
        user_obj = info.context.user[0]
        if user_obj.is_superuser != True and user_obj.is_staff != True:
            raise Exception("Not Allowed")
        holyday = Holydays.objects.get(pk = id)
        holyday.delete()
        return DeleteHolyday(success = True)

class HolydayMutation(ObjectType):
    create_holyday = CreateHolyday.Field()
    update_holyday = UpdateHolyday.Field()
    delete_holyday = DeleteHolyday.Field()
        