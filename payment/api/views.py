from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from account.api.serializer import *
from rest_framework import status
from django.db.models import Q

from villa.models import Villa
from account.models import Account

@api_view(['POST'])
def charge(request):
    user = request.user

    if 'currency' not in request.data.keys():
        return Response({'message':'currency field required'},
                         status=status.HTTP_400_BAD_REQUEST)
    
    user.currency += float(request.data['currency'])
    user.save()
    return Response({"message":'charging currency successfully'},
                     status=status.HTTP_200_OK)


@api_view(['POST'])
def pay(request):
    user = request.user
    admin = Account.objects.get(email='admin@admin.com')

    if 'currency' not in request.data.keys():
        return Response({'message':'currency field required'},
                         status=status.HTTP_400_BAD_REQUEST)

    else:
        currency = float(request.data['currency'])

    if 'villa' not in request.data.keys():
        return Response({'message':'villa field required'},
                         status=status.HTTP_400_BAD_REQUEST)
    else:
        try:
            villa = Villa.objects.get(villa_id=int(request.data['villa']))
            owner = villa.owner
        except Exception as e:
            return Response(e,status=status.HTTP_404_NOT_FOUND)

    if currency > user.currency:
        return Response({'message':'required more currency'},
                         status=status.HTTP_406_NOT_ACCEPTABLE)

    user.currency -= currency
    user.save()
    admin.currency += (currency / 10)
    admin.save()
    owner.currency += 0.9 * currency
    owner.save()
    return Response({'message':'paying successfully'},
                     status=status.HTTP_200_OK)