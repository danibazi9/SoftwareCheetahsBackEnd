from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.response import Response
from chat.models import Message
import datetime
from account.models import Account

@api_view(['POST'])
def show_Message(request):
    user = request.user
    contact = Account.objects.get(uset_id=request.GET['contact'])
    message = Message.objects.filter(account1=user, account2=contact)
    datalist = []
    for i in range(len(message)):
        data = {
            'user': message[i].user.id,
            'message_id': message[i].id,
            'username': message[i].user.username,
            'text': message[i].text,
            'time': message[i].time.ctime(),
        }
        if message[i].parentMessage:
            # if message[i].id == None:
            data['replyTo'] = message[i].parentMessage.id
        datalist.append(data)
    return Response(datalist, status=status.HTTP_200_OK)
