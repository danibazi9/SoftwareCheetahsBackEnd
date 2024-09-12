from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.response import Response
from django.db.models import Q

from chat.models import Chat, Message
from .serializer import ChatAccountSerializer, MessageSerializer
from account.models import Account

from datetime import datetime

@api_view(['POST'])
def add_chat(request):
    user = request.user
    if 'contact' in request.data.keys():
        try:
            contact = Account.objects.get(user_id=request.data['contact'])
        except:
            return Response({'message':'contact does not exist'},
                              status=status.HTTP_404_NOT_FOUND)
    else:
        return Response({'message':'contact field is required !'},
                          status=status.HTTP_400_BAD_REQUEST)

    if user == contact:
        return Response({'message':'user and contact is equal !'},
                         status=status.HTTP_406_NOT_ACCEPTABLE)

    query = (Q(account1=user) & Q(account2=contact))

    query = query | (Q(account1=contact) & Q(account2=user))       
    try:
        chat = Chat.objects.get(query)
        serializer = ChatAccountSerializer(chat.account2)
        data = serializer.data
        data['chat_id'] = chat.chat_id
        return Response({'message':'this chat is already existed', 'data':data},
                         status=status.HTTP_208_ALREADY_REPORTED)
    except:
        chat = Chat.objects.create(
            account1=user,
            account2=contact
        )
        chat.save()
        serializer = ChatAccountSerializer(chat.account2)
        data = serializer.data
        data['chat_id'] = chat.chat_id
        return Response({'message':'add chat successfully', 'data':data},
                        status=status.HTTP_200_OK)


@api_view(["GET"])
def show_chat(request):
    user = request.user
    data = []

    query = Q(account1=user)
    chats = Chat.objects.filter(query)
    for c in chats:
        serializer = ChatAccountSerializer(c.account2)
        d = serializer.data
        d['chat_id'] = c.chat_id
        try:
            last_message = Message.objects.filter(chat=c).latest('message_id')
        except:
            last_message = None
        if last_message == None:
            d['last_message'] = None
        else:
            message_serializer = MessageSerializer(last_message)
            d['last_message'] = message_serializer.data
        data.append(d)


    query = Q(account2=user)
    chats = Chat.objects.filter(query)
    for c in chats:
        serializer = ChatAccountSerializer(c.account1)
        d = serializer.data
        d['chat_id'] = c.chat_id
        try:
            last_message = Message.objects.filter(chat=c).latest('message_id')
        except:
            last_message = None
        if last_message == None:
            d['last_message'] = None
        else:
            message_serializer = MessageSerializer(last_message)
            d['last_message'] = message_serializer.data
        data.append(d)

    return Response({'message':'show chats successfuly', 'data':data},
                     status=status.HTTP_200_OK)

@api_view(['POST'])
def upload_file(request):
    user = request.user
    if 'chat_id' in request.data.keys():
        try:
            chat = Chat.objects.get(chat_id=request.data['chat_id'])
        except:
            return Response({'message':'This chat does not exist'},
                            status=status.HTTP_404_NOT_FOUND)
    else:
        return Response({'message':'chat_id field needed'},
                         status=status.HTTP_400_BAD_REQUEST)

    if 'image' in request.FILES.keys():
        image = request.FILES['image']
    else:
        image = None
    if 'file' in request.FILES.keys():
        file = request.FILES['file']
    else:
        file = None
        
    message = Message.objects.create(
        chat=chat,
        owner=user,
        image=image,
        file=file,
        time = datetime.now()
    )

    serializer = MessageSerializer(message)
    message.save()
    return Response({'message':'upload image or file successfully', 'data':serializer.data},
                     status=status.HTTP_200_OK)