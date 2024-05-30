from graphene import ObjectType, List, JSONString
from .models import Message
from .types import UserMessageType, MessageType
from django.db.models import Q
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