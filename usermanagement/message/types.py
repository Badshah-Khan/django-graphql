from graphene_django import DjangoObjectType
from .models import Message
from user.types import UserType
from graphene import ObjectType, Field, InputObjectType, Int, String, DateTime, List, Boolean

class MessageInput(InputObjectType):
    receiver_id = Int(required = True)
    date = DateTime(required = True)
    content = String(required = True)
    attachments = List(String)
    organization = Int(required = True)

class MessageUpdateInput(InputObjectType):
    date = DateTime(required = True)
    content = String(required = True)
    is_read = Boolean()

class MessageType(ObjectType):
    id = Int()
    sender_id = Int()
    receiver_id = Int()
    date = DateTime()
    content = String()
    is_read = Boolean()
    is_deleted = Boolean()
    is_accepted = Boolean()
    organization = Int()

class MessageUserType(ObjectType):
    user = Field(UserType)
    message = Field(MessageType)

class UserMessageType(ObjectType):
    user_id = Int()
    first_name = String()
    last_name = String()
    profile = String()
    content = String()
    date = DateTime()
    id = Int()