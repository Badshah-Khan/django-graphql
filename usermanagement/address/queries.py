from graphene import ObjectType, List, JSONString, Int, String, Field
from .models import Address
from usermanagement.utils import camel_to_kebab
from organization.types import OrgAddressType
from .types import AddressType
from django.db.models import Q
from usermanagement.utils import system_user


class AddressQuery(ObjectType):
    addresses = List(OrgAddressType, where = JSONString(), limit = Int(), offset = Int(), order = String())
    address= Field(AddressType, id = Int(required = True))

    def resolve_addresses(self, info, where = None, limit = 100, offset = 0, order = None):
        system_user(info)
        orderBy = "street"
        if order is not None:
            orderBy = order.split(" ")[0]
            dir = order.split(" ")[1]
        orders = '-' if dir == 'desc' else ''
        search = ''
        if where is not None:
            search = where.get('search', '')
        result = Address.objects.filter(Q(street__icontains=search) | Q(city__icontains = search) | Q(state__icontains = search) | Q(country__icontains = search))
        result = result.order_by(f'{orders}{camel_to_kebab(orderBy)}')[offset:offset + limit]

        address_data = [{'address': item, 'organization': item.organization} for item in result]

        return address_data
    
    def resolve_address(self, info, id):
        system_user(info)
        return Address.objects.get(pk = id)
