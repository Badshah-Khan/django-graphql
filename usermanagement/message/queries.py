from graphene import ObjectType, List, JSONString, Field, Int
from .models import Message
from .types import UserMessageType, MessageType
from django.db.models import Q
from channels.layers import get_channel_layer
from .common import Common
from usermanagement.utils import user_authentication, organization_validation

class MessageQuery(ObjectType):
    messages = List(MessageType, where = JSONString())
    user_message = List(UserMessageType, where = JSONString())

    def resolve_messages(self, info, where):
        user_obj = user_authentication(info)
        user_org = organization_validation(info)
        sender_id = where.get('sender', None)
        if sender_id is None:
            raise Exception('Something went wrong!')
        result = Message.objects.filter(Q(organization = user_org) & Q(is_deleted = False) 
            & ((Q(receiver_id = user_obj.id) & Q(sender_id = sender_id)) | (Q(receiver_id = sender_id) & Q(sender_id = user_obj.id)) ))
        return result
    
    def resolve_user_message(self, info, where = None):
        user_obj = user_authentication(info)
        user_org = organization_validation(info)
        result = Common().users_list(user_obj.id, user_org)
        return result
    
class MessageSubscription(ObjectType):
    new_message = Field(MessageType, sender_id = Int())
    # new_user = List(UserMessageType, where = JSONString())

    async def resolve_new_message(root, info, sender_id):
        print("subscription")
        is_auth = info.context.is_auth
        if not is_auth:
            raise Exception("Unauthorized")

        message = Message.objects.get(Q(sender_id = sender_id) | Q(receiver_id = sender_id))

        channel_layer = get_channel_layer()
        await channel_layer.group_send(
            "chat_netforth",
            {
                'type': 'chat.message',
                'message': {
                    'id': message.id,
                    'content': message.content,
                    'sender_id': message.sender_id,
                    'receiver_id': message.receiver_id,
                    'date': message.date,
                    'is_read': message.is_read,
                    'is_deleted': message.is_deleted,
                    'is_accepted': message.is_accepted,
                }
            }
        )
        
        return message