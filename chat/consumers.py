import json
from channels.generic.websocket import AsyncWebsocketConsumer
import datetime
from channels.db import database_sync_to_async

from .models import Message, Chat
from account.models import Account
from rest_framework.authtoken.models import Token

from .api.serializer import MessageSerializer
import jwt


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print(self.scope['headers'])
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        self.user = None
        self.chat = self.room_name
        print(self.chat)

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        data = json.loads(text_data)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            data,
        )

    # Receive message from room group
    async def create(self, event):
        # Send message to WebSocket
        #responce = await self.create_message(event=event)
        responce = {}
        await self.send(text_data=json.dumps(responce))

    async def authenticate(self, event):
        responce = await self.authenticate_user(event=event)
        await self.send(text_data=json.dumps(responce))


    @database_sync_to_async
    def authenticate_user(self , event):
        try:
            account_id = Token.objects.get(key=event['Authorization']).user_id
            self.user = Account.objects.get(user_id=account_id)
            return {'message' : 'authentication is completed !', 'data' : self.user.email}
        except:
            return {'message' : 'invalid token'}

    @database_sync_to_async
    def create_message(self , event):
        print(event)
        if self.user == None:
            return {'message': 'authenticate needed.', "data":None}

        try:
            chat = Chat.objects.get(id=event['chat_id'])
        except:
            return {'message': f"chat {event['chat_id']} does not exist", "data":None}

        try:
            owner = Account.objects.get(id=event['user_id'])
        except:
            return {'message': f"owner {event['user_id']} does not exist", "data":None}

        try:
            parent_message = Message.objects.get(id=event['parent_message'])
        except:
            return {'message': f"message {event['parent_message']} does not exist", "data":None}

        message = Message.objects.create(
            chat=chat,
            owner=owner,
            text=event['message'],
            parent_message=parent_message,
            time = datetime.datetime.now()
        )

        serializer = MessageSerializer(message)
        message.save()
        return {'message':'create message successfully', 'data':serializer.data}

    @database_sync_to_async
    def delete_message(self , event):
        data = {}
        chatroom = Chat.objects.filter(id=event['chatroom_id'])
        user = Account.objects.filter(id=event['user_id'])
        if user[0] == chatroom[0].owner:
            message = Message.objects.filter(
                id=event['message_id']
            )
            if list(message) == []:
                data['message'] = 'message not found'
            else:
                data['message_id']=message[0].id
                message[0].delete()
                data['message'] = 'message delete successfully'
                
        else:
            data['message'] = 'user is not owner'
        data['type'] = 'chat_message'
        data['order_type'] = 'delete_message'
        print(data)
        return data
    