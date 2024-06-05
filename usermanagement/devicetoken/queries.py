from graphene import ObjectType, List, JSONString
from .types import DeviceTokenType
from .models import DeviceToken
from usermanagement.utils import user_authentication, organization_validation

class DeviceTokenQuery(ObjectType):
    device_tokens = List(DeviceTokenType, where = JSONString())

    def resolve_device_tokens(self, info, where = None):
        user_authentication(info)
        organization = organization_validation(info)

        tokens = DeviceToken.objects.filter(organization_id = organization)
        if where is not None:
            user_id = where.get('user_id', None)
            if user_id is not None:
                tokens = tokens.filter(user_id = user_id)
        return tokens