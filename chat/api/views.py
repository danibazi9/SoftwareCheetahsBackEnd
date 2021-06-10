from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.response import Response
from django.db.models import Q

from chat.models import Chat
from .serializer import ChatAccountSerializer
from account.models import Account

@api_view(['POST'])
def add_chat(request):
    user = request.user
    if 'contact' in request.POST.keys():
        try:
            contact = Account.objects.get(user_id=request.POST['contact'])
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
        data.append(d)


    query = Q(account2=user)
    chats = Chat.objects.filter(query)
    for c in chats:
        serializer = ChatAccountSerializer(c.account1)
        d = serializer.data
        d['chat_id'] = c.chat_id
        data.append(d)

    return Response({'message':'show chats successfuly', 'data':data},
                     status=status.HTTP_200_OK)


@api_view(['GET'])
def add_chat(request):
    user = request.user
    if 'contact' in request.POST.keys():
        try:
            contact = Account.objects.get(user_id=request.POST['contact'])
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
        return Response({'message':'chat does not'})