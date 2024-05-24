from graphene import Mutation, Boolean, Field, Int, ObjectType
from .models import Address
from .types import AddressType, AddressOrgInputType, AddressUpdateInput
from organization.models import Organization
from usermanagement.utils import super_staff_authorization, system_user, organization_validation

class CreateAddress(Mutation):
    class Arguments:
        input = AddressOrgInputType(required = True)

    success = Boolean()

    def mutate(self, info, input):
        user_obj = super_staff_authorization(info)
        organization = organization_validation(info, input['organization'] if user_obj.is_staff else None)
        del input['organization']
        Address.objects.create(**input, organization = Organization.objects.get(pk = organization))
        return CreateAddress(success=True)

class UpdateAddress(Mutation):
    class Arguments:
        id = Int(required=True)
        input = AddressUpdateInput(required = True)

    success = Boolean()
    address = Field(AddressType)

    def mutate(self, info, id, input):
        super_staff_authorization(info)
        address = Address.objects.get(pk=id)
        if input.street:
            address.street = input.street
        if input.city:
            address.city = input.city
        if input.postal_code:
            address.postal_code = input.postal_code
        if input.state:
            address.state = input.state
        if input.country:
            address.country = input.country
        if input.organization:
            address.organization = input.organization

        address.save()
        return UpdateAddress(success=True, address = address)
    
class DeleteAddress(Mutation):
    class Arguments:
        id = Int(required=True)

    success = Boolean()

    def mutate(self, info, id):
        system_user(info)
        address = Address.objects.get(pk=id)
        address.delete()
        return DeleteAddress(success=True)
    
class AddressMutation(ObjectType):
    create_address = CreateAddress.Field()
    update_address = UpdateAddress.Field()
    delete_address = DeleteAddress.Field()