from graphene import InputObjectType, ObjectType, String, Boolean, Int

class DeviceTokenInput(InputObjectType):
    device_token = String(required = True)
    device_type = String(required = True)
    device_id = String(required = True)
    app_version = String()
    os_version = String(required = True)
    is_active = Boolean()

class DeviceTokenType(ObjectType):
    id = Int()
    device_token = String()
    device_type = String()
    device_id = String()
    app_version = String()
    os_version = String()
    is_active = Boolean()
    user_id = Int()