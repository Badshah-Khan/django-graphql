from graphene import Mutation, String, Boolean, Field, Int, ObjectType
from .models import Address
from .types import AddressType, AddressOrgInputType
from organization.models import Organization

class CreateAddress(Mutation):
    class Arguments:
        input = AddressOrgInputType(required = True)

    success = Boolean()

    def mutate(self, info, input):
        is_auth = info.context.is_auth
        if not is_auth:
            raise Exception("Unauthorized")
        user_obj = info.context.user[0]
        if user_obj.is_superuser != True:
            raise Exception("Not Allowed")
        token_obj = info.context.user[1]
        organization = token_obj['data']['organization']
        if user_obj.is_staff == True and organization != input.organization:
            raise Exception("Not Allowed")
        del input['organization']
        Address.objects.create(**input, organization = Organization.objects.get(pk = organization))
        return CreateAddress(success=True)

class UpdateAddress(Mutation):
    class Arguments:
        address_id = Int(required=True)
        street = String()
        city = String()
        postal_code = String()
        state = String()
        country = String()
        organization = Int()

    success = Boolean()
    address = Field(AddressType)

    def mutate(self, info, address_id, street=None, city=None, postal_code=None, state=None, country=None, organization=None):
        address = Address.objects.get(pk=address_id)
        if street:
            address.street = street
        if city:
            address.city = city
        if postal_code:
            address.postal_code = postal_code
        if state:
            address.state = state
        if country:
            address.country = country
        if organization:
            address.organization = organization

        address.save()
        return UpdateAddress(success=True, address = address)
    
class DeleteAddress(Mutation):
    class Arguments:
        address_id = Int(required=True)

    success = Boolean()

    def mutate(self, info, address_id):
        address = Address.objects.get(pk=address_id)
        address.delete()
        return DeleteAddress(success=True)
    
class AddressMutation(ObjectType):
    create_address = CreateAddress.Field()
    update_address = UpdateAddress.Field()
    delete_address = DeleteAddress.Field()