import json
from os import environ
from channels.generic.websocket import AsyncWebsocketConsumer
import datetime
from channels.db import database_sync_to_async
from asgiref.sync import sync_to_async
from django.http import response

from .models import Message, Chat
from account.models import Account
from rest_framework.authtoken.models import Token

from .api.serializer import MessageSerializer
import jwt


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        self.user = None
        self.chat = await self.get_chat(self.room_name)

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
        response = await self.handle_order(data)

        if data['type'] not in ['fetch', 'authenticate']:
        # Send message to room group
            await self.channel_layer.group_send(
                self.room_group_name,
                response,
            )
            
        else:
            await self.send(text_data=json.dumps(response))

    # Receive message from room group
    async def chat_message(self, event):
       # Send message to WebSocket
        await self.send(text_data=json.dumps(event))
       



    async def handle_order(self, event):
        if event['type'] == 'update':
            responce = await self.update_message(event)
        elif event['type'] == 'fetch':
            responce = await self.fetch_message(event)
        elif event['type'] == 'create':
            responce = await self.create_message(event)
        elif event['type'] == 'delete':
            responce = await self.delete_message(event)
        elif event['type'] == 'authenticate':
            responce = await self.authenticate_user(event)
        responce['type'] = 'chat_message'

        return responce
 

    @sync_to_async
    def get_chat(self, chat_id):
        return Chat.objects.get(chat_id=chat_id)


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
        if self.user == None:
            return {'message': 'authenticate needed.', "data":None}

        if 'parent_message' in event.keys():
            try:
                parent_message = Message.objects.get(message_id=event['parent_message'])
            except:
                return {'message': f"message {event['parent_message']} does not exist", "data":None}
        else:
            parent_message = None

        message = Message.objects.create(
            chat=self.chat,
            owner=self.user,
            text=event['message'],
            parent_message=parent_message,
            time = datetime.datetime.now()
        )

        serializer = MessageSerializer(message)
        message.save()
        return {'message':'create message successfully', 'data':serializer.data}


    @database_sync_to_async
    def delete_message(self , event):
        if self.user == None:
            return {'message': 'authenticate needed.', "data":None}

        try:
            message = Message.objects.get(message_id=event["message_id"])
        except:
            return {'message':'this message does not exist'}

        message.delete()
        return {'message':'delete message successfully',
                'data':{'message_id':event['message_id']}}


    @database_sync_to_async
    def fetch_message(self, event):
        if self.user == None:
            return {'message': 'authenticate needed.', "data":None}

        messages = Message.objects.filter(chat=self.chat)
        serializer = MessageSerializer(messages, many=True)
        return {'message':'fetch successfully', 'data':serializer.data}


    @database_sync_to_async
    def update_message(self, event):
        if self.user == None:
            return {'message': 'authenticate needed.', "data":None}

        try:
            message = Message.objects.get(message_id=event["message_id"])
        except:
            return {'message':'this message does not exist'}

        if 'text' in event.keys():
            message.text = event['text']

        serializer = MessageSerializer(message)
        message.save()

        return {'message':'update message successfully', 'data':serializer.data}
                
    