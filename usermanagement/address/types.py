from .models import Address
from graphene_django import DjangoObjectType
from graphene import relay

class AddressType(DjangoObjectType):
    class Meta:
        model = Address
        fields = '__all__'
        filter_fields = {
            'street': ['exact', 'icontains'],
            'city': ['exact', 'icontains'],
            'postal_code': ['exact'],
            'state': ['exact', 'icontains'],
            'country': ['exact', 'icontains'],
            'organization': ['exact']
        }
        interfaces = (relay.Node,)
