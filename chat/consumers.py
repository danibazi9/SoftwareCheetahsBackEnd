import json
from channels.generic.websocket import AsyncWebsocketConsumer
import datetime
from channels.db import database_sync_to_async

from .models import Message
from account.models import Account
from .serializer import MessageSerializer
import jwt


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        text_data_json['type'] = 'chat_message'
        decodedPayload = jwt.decode(text_data_json['token'],None,None)
        text_data_json['user_id'] = decodedPayload['user_id']
        # print(decodedPayload)
        data = {}
        if text_data_json['order_type'] == 'create_message':
            data = await self.create_message(event=text_data_json)
        elif text_data_json['order_type'] == 'delete_message':
            data = await self.delete_message(event=text_data_json)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            data,
        )

    # Receive message from room group
    async def chat_message(self, event):
        print(event)
        # Send message to WebSocket
        await self.send(text_data=json.dumps(event))
    @database_sync_to_async
    def create_message(self , event):
        print(event)
        chatroom = Chatroom.objects.filter(id=event['chatroom_id'])
        user = User.objects.filter(id=event['user_id'])
        message = Message.objects.create(
            chatroom=chatroom[0],
            user=user[0],
            text=event['message'],
            time = datetime.datetime.now()
        )
        # message.save()
        serializer = MessageSerializer(message)
        data = serializer.data
        data["time"] = message.time.ctime()
        # for detect type of data
        data['type'] = 'chat_message'
        data['order_type'] = 'create_message'
        data['message_id'] = message.id
        data['username'] = user[0].username
        if 'replyTo' in event.keys() :
            replyMessage = Message.objects.filter(id=event['replyTo'])
            message.parentMessage = replyMessage[0]
            data['replyTo'] = replyMessage[0].id
        message.save()
        # if message.parentMessage != None:
        #     data['replyTo'] = message.parentMessage
        return data

    @database_sync_to_async
    def delete_message(self , event):
        data = {}
        chatroom = Chatroom.objects.filter(id=event['chatroom_id'])
        user = User.objects.filter(id=event['user_id'])
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
    