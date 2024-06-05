from graphene import Mutation, Boolean, ObjectType
from .types import DeviceTokenInput
from .models import DeviceToken
from usermanagement.utils import user_authentication, organization_validation

class CreateDeviceToken(Mutation):
    class Arguments:
        input = DeviceTokenInput(required = True)
    success = Boolean()

    def mutate(self, info, input):
        user_obj = user_authentication(info)
        user_org = organization_validation(info)

        try:
            DeviceToken.objects.get(user_id = user_obj.id, device_id = input.device_id, device_type = input.device_type)
        except DeviceToken.DoesNotExist:
            DeviceToken.objects.create(**input, user_id = user_obj.id, organization_id = user_org)
        return CreateDeviceToken(success = True)

class DeviceTokenMutation(ObjectType):
    create_device_token = CreateDeviceToken.Field()