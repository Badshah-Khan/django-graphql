from graphene import Mutation, ObjectType, Boolean, Int
from .types import HolydayInput
from .models import Holydays
from usermanagement.utils import super_staff_authorization, organization_validation

class CreateHolyday(Mutation):
    class Arguments:
        input = HolydayInput(required = True)
    
    success = Boolean()

    def mutate(self, info, input):
        super_staff_authorization(info)
        organization = input.get('organization')
        organization_validation(info, organization)
        del input['organization']
        Holydays.objects.create(**input, organization_id = organization)

        return CreateHolyday(success = True)

class UpdateHolyday(Mutation):
    class Arguments:
        input = HolydayInput(required = True)
        id = Int(required = True)
    success = Boolean()

    def mutate(self, info, input, id):
        super_staff_authorization(info)
        organization = input.get('organization')
        organization_validation(info, organization)
        del input['organization']

        holyday = Holydays.objects.get(pk= id)

        return UpdateHolyday(success = True)

class DeleteHolyday(Mutation):
    class Arguments:
        id = Int(required = True)
    success = Boolean()

    def mutate(self, info, id):
        super_staff_authorization(info)
        holyday = Holydays.objects.get(pk = id)
        holyday.delete()
        return DeleteHolyday(success = True)

class HolydayMutation(ObjectType):
    create_holyday = CreateHolyday.Field()
    update_holyday = UpdateHolyday.Field()
    delete_holyday = DeleteHolyday.Field()
        