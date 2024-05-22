from channels.generic.websocket import AsyncWebsocketConsumer
import json
from urllib.parse import parse_qs
from message.models import Message
from userstatus.models import UserStatus
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import TokenError
from channels.db import database_sync_to_async
from datetime import datetime
from .common import Common
from django.db.models import Q
    
class SubscriptionConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        query_params = parse_qs(self.scope['query_string'].decode('utf-8'))
        token = query_params.get('token', [''])[0]
        self.user = ''
        if token == '':
            return await self.close()
        user = verify_token(token)
        if user == False:
            await self.close()
        else:
            self.user = user.get('user_id')
            org_data = user.get('data')
            self.organization = org_data.get('organization')
            await self.set_user_online()
            await self.channel_layer.group_add(
                f"user_{self.user}",
                self.channel_name
            )
            await self.accept()
            online_users = await self.get_online_user()
            await self.send(text_data=json.dumps({
                'message': 'Welcome! You are now connected.',
                'online_users': online_users,
                'users': await self.get_users(self.user)
            }))

    async def disconnect(self, close_code):
        await self.set_user_offline()
        await self.channel_layer.group_discard(
            f"user_{self.user}",
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        receiver_id = data['receiver_id']
        new_message =  await self.create_message(message, receiver_id)
        if receiver_id != self.user:
            user_list = await self.get_users(receiver_id)
            await self.channel_layer.group_send(
                f"user_{receiver_id}",
                {
                    "type": "chat.message",
                    "users": user_list,
                    "message": {
                        'content': new_message.content,
                        'id': new_message.id,
                        'date': new_message.date,
                        'receiverId': new_message.receiver_id,
                        'senderId': new_message.sender_id,
                        'isRead': new_message.is_read
                    },
                }
            )
        user_list = await self.get_users(self.user)
        await self.send(text_data=json.dumps({
            'type': 'message',
            'message': {
                    'content': new_message.content,
                    'id': new_message.id,
                    'date': new_message.date,
                    'receiverId': new_message.receiver_id,
                    'senderId': new_message.sender_id,
                    'isRead': new_message.is_read
                },
            'users': user_list
        }))
            
    async def chat_message(self, event):
        message = event['message']
        users = event['users']
        await self.send(text_data=json.dumps({
            'type': 'message',
            'users': users,
            'message': message
        }))

    @database_sync_to_async
    def set_user_online(self):
        try:
            user_status = UserStatus.objects.get(user_id = self.user)
            user_status.is_online = True
            user_status.save()
        except UserStatus.DoesNotExist:
            user_status = UserStatus.objects.create(user_id = self.user, organization_id = self.organization, is_online = True)
        return user_status

    @database_sync_to_async
    def set_user_offline(self):
        try:
            user_status = UserStatus.objects.get(user_id = self.user)
            user_status.is_online = False
            user_status.last_seen = datetime.now()
            user_status.save()
        except UserStatus.DoesNotExist:
            user_status = UserStatus.objects.create(
                user_id = self.user, 
                organization_id = self.organization, 
                is_online = False, 
                last_seen = datetime.now()
            )
        return user_status

    @database_sync_to_async
    def get_online_user(self):
        user_ids = UserStatus.objects.filter(is_online = True).exclude(user_id=self.user).values_list('user_id', flat=True)
        return list(user_ids)
    
    @database_sync_to_async
    def get_receiver_user(self, id):
        try:
            user_status = UserStatus.objects.get(user_id = id)
        except UserStatus.DoesNotExist:
            user_status = UserStatus.objects.create(
                user_id = self.user, 
                organization_id = self.organization, 
                is_online = False, 
                last_seen = datetime.now()
            )
        return user_status.is_online

    @database_sync_to_async
    def create_message(self, message, receiver_id):
        return Message.objects.create(
            content=message['content'],
            date=message['date'],
            organization_id=self.organization,
            sender_id= self.user,
            receiver_id=receiver_id
        )
    
    @database_sync_to_async
    def get_users(self, user_id):
        user_list = Common().users_list(user_id, self.organization)
        result = [{
            'id': item.id,
            'userId': item.user_id, 
            'senderId': item.sender_id, 
            'receiverId': item.receiver_id, 
            'content': item.content, 
            'date': item.date.strftime('%Y-%m-%d %H:%M:%S'), 
            'profile': item.profile, 
            'firstName': item.first_name, 
            'lastName': item.last_name
            } for item in user_list]
        return result
    
class TypingConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        query_params = parse_qs(self.scope['query_string'].decode('utf-8'))
        token = query_params.get('token', [''])[0]
        self.user = ''
        if token == '':
            return await self.close()
        user = verify_token(token)
        if user == False:
            await self.close()
        else:
            self.user = user.get('user_id')
            org_data = user.get('data')
            self.organization = org_data.get('organization')
            await self.channel_layer.group_add(
                f"typing_{self.user}",
                self.channel_name
            )
            await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        data = json.loads(text_data)
        typing = data['typing']
        receiver_id = data['receiver_id']
        print("typing", typing)
        await self.channel_layer.group_send(
            f"typing_{receiver_id}",
            {
                "type": "typing.message",
                "typing": typing
            }
        )

    async def typing_message(self, event):
        typing = event['typing']
        await self.send(text_data=json.dumps({
            'type': 'typing',
            'typing': typing
        }))

def verify_token(token):
    try:
        access_token = AccessToken(token)
        return access_token.payload
    except TokenError:
        return False