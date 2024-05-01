from .models import Address
from graphene_django import DjangoObjectType
from graphene import relay, InputObjectType, String, Int

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

class AddressOrgInputType(InputObjectType):
    street = String(required = True)
    city = String(required = True)
    postal_code = String(required = True)
    state = String(required = True)
    country = String(required = True)
    organization = Int()
    lat = String()
    long = String()
