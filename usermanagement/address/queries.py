from graphene import ObjectType

from graphene_django.filter import DjangoFilterConnectionField
from .models import Address
from .types import AddressType


class AddressQuery(ObjectType):
    addresses = DjangoFilterConnectionField(AddressType)

    def resolve_addresses(self, info, **kwargs):
        return Address.objects.all()
