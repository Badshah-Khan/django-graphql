from graphene import ObjectType, List, JSONString, Field, Int
from .models import Message
from .types import MessageUserType, UserMessageType, MessageType
from .consumers import SubscriptionConsumer
from django.db.models import Q

class MessageQuery(ObjectType):
    messages = List(MessageType, where = JSONString())
    user_message = List(UserMessageType, where = JSONString())

    def resolve_messages(self, info, where):
        is_auth = info.context.is_auth
        if not is_auth:
            raise Exception("Unauthorized")
        user_obj = info.context.user[0]
        token_obj = info.context.user[1]
        user_org = token_obj['data']['organization']
        sender_id = where.get('sender', None)
        if sender_id is None:
            raise Exception('Something went wrong!')
        result = Message.objects.filter(Q(organization = user_org) 
            & ((Q(receiver_id = user_obj.id) & Q(sender_id = sender_id)) | (Q(receiver_id = sender_id) & Q(sender_id = user_obj.id)) ))
        return result
    
    def resolve_user_message(self, info, where = None):
        is_auth = info.context.is_auth
        if not is_auth:
            raise Exception("Unauthorized")
        user_obj = info.context.user[0]
        token_obj = info.context.user[1]
        user_org = token_obj['data']['organization']
        query = '''WITH RankedMessages AS (
            SELECT
                mm.id,
                mm.sender_id,
                mm.receiver_id,
                mm.content,
                mm.date,
                au.id AS user_id,
                au.first_name,
                au.last_name,
                ee.profile,
                ROW_NUMBER() OVER (PARTITION BY au.id ORDER BY mm.date DESC) AS message_rank
            FROM
                message_message mm
            LEFT JOIN
                auth_user au ON mm.receiver_id = au.id OR mm.sender_id = au.id
            LEFT JOIN
            employeedetails_employee ee ON ee.user_id = au.id
            where mm.organization_id = %s
            )
            SELECT
                id,
                user_id,
                sender_id,
                receiver_id,
                content,
                date,
                profile,
                first_name,
                last_name
            FROM
                RankedMessages
            WHERE
                message_rank = 1 and user_id != %s;
        '''
        parameters = []
        parameters.extend([user_org, user_obj.id])
        result = Message.objects.raw(query, parameters)
        return result
    
class MessageSubscription(ObjectType):
    new_message = Field(MessageUserType)

    async def resolve_new_message(root, info):
        # Instantiate WebSocket consumer
        consumer = SubscriptionConsumer()

        # Subscribe the consumer to new message updates
        # (Subscription logic depends on your application design)

        # Send subscription confirmation message
        await consumer.send_update({'message': 'Subscribed to new messages.'})

        # Implement any cleanup logic when the subscription ends
        # For example, unsubscribe the consumer from updates

        # Return the consumer
        return consumer