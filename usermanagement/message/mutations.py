from graphene import Mutation, Boolean, Int,  ObjectType, DateTime
from .models import Message
from .types import MessageInput, MessageUpdateInput

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
        print(input)
        Message.objects.create(**input, organization_id = organization, sender_id = user_obj.id)
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
        id = Int(required=True)
        deleted_at = DateTime(required = True)
    success = Boolean()

    def mutate(self, info, id):
        message = Message.objects.get(pk=id)
        message.delete()
        return DeleteMessage(success=True)
    
class MessageMutation(ObjectType):
    send_message = SendMessage.Field()
    update_message = UpdateMessage.Field()
    delete_message = DeleteMessage.Field()