from graphene import Mutation, String, Boolean, Field, Int, ObjectType
from .models import Address
from .types import AddressType

class CreateAddress(Mutation):
    class Arguments:
        street = String(required = True)
        city = String(required = True)
        postal_code = String(required = True)
        state = String(required = True)
        country = String(required = True)
        organization = Int(required = True)

    success = Boolean()
    address = Field(AddressType)

    def mutate(self, info, street, city, postal_code, state, country, organization):
        address = Address.objects.create(street=street, city=city, postal_code=postal_code, state=state, country=country, organization=organization)
        return CreateAddress(success=True, organization=address)

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