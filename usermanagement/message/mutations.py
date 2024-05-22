from graphene import Mutation, Boolean, Int,  ObjectType, DateTime, List
from .models import Message
from .types import MessageInput, MessageUpdateInput
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from datetime import datetime

class SendMessage(Mutation):
    class Arguments:
        input = MessageInput(required = True)
    success = Boolean()

    def mutate(self, info, input):
        is_auth = info.context.is_auth
        if not is_auth:
            raise Exception("Unauthorized")
        user_obj = info.context.user[0]
        token_obj = info.context.user[1]
        user_org = token_obj['data']['organization']
        organization = input.get('organization')
        del input['organization']
        if organization != user_org:
            raise Exception("Wrong organization")
        message = Message.objects.create(**input, organization_id = organization, sender_id = user_obj.id)
        print("before channel")
        channel_layer = get_channel_layer()
        print("channel_layer",channel_layer)
        message_data = {
            'type': 'chat.message',
            'message': {
                'id': message.id,
                'content': message.content,
                'sender_id': message.sender_id,
                'receiver_id': message.receiver_id,
                'date': message.date.isoformat(),
                'is_read': message.is_read,
                'is_deleted': message.is_deleted,
                'is_accepted': message.is_accepted,
            }
        }
        async_to_sync(channel_layer.group_send)("chat_netforth", message_data)
        return SendMessage(success=True)

class UpdateMessage(Mutation):
    class Arguments:
        id = Int(required = True)
        input = MessageUpdateInput(required = True)

    success = Boolean()
    def mutate(self, info, id, input):
        message = Message.objects.get(pk=id)
        
        if input.is_read:
            message.is_read = input.is_read
        message.save()
        return UpdateMessage(success=True)
    
class DeleteMessage(Mutation):
    class Arguments:
        id = List(Int, required = True)
        deleted_at = DateTime(required = True)
    success = Boolean()

    def mutate(self, info, id, deleted_at):
        message = Message.objects.filter(pk__in=id)
        message.update(is_deleted = True, deleted_at = deleted_at)
        return DeleteMessage(success=True)
    
class MessageMutation(ObjectType):
    send_message = SendMessage.Field()
    update_message = UpdateMessage.Field()
    delete_message = DeleteMessage.Field()