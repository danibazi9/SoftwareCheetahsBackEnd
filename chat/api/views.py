from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.response import Response
from chat.models import Message, Chat
import datetime
from account.models import Account

@api_view(['POST'])
def add_chat(request):
    user = request.user
    if 'contact' in request.POST.keys():
        try:
            contact = Account.objects.get(uset_id=request.POST['contact'])
        except:
            return Response({'message':'contact does not exist'},
                              status=status.HTTP_404_NOT_FOUND)
    else:
        return Response({'message':'contact field is required !'},
                          status=status.HTTP_400_BAD_REQUEST)

    if user == contact:
        return Response({'message':'user and contact is equal !'},
                         status=status.HTTP_406_NOT_ACCEPTABLE)

    chat = Chat.objects.create(
        account1=user,
        account2=contact
    )
    chat.save()

    return Response({'message':'add chat successfully'}, status=status.HTTP_200_OK)
