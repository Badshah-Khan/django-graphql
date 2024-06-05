from graphene import InputObjectType, ObjectType, String, Boolean, DateTime, Int

class NotificationInput(InputObjectType):
    type = String(required = True)
    title = String()
    message = String(required = True)
    priority = String()
    expiration_date = DateTime(required = True)

class NotificationType(ObjectType):
    id = Int()
    user_id = Int()
    type = String()
    title = String()
    message = String()
    status = String()
    priority = String()
    is_read = Boolean()
    read_at = DateTime()
    error_message = String()
    url = String()
    expiration_date = DateTime()
    action_required = Boolean()
    created_at = DateTime()
    updated_at = DateTime()
    organization_id = Int()