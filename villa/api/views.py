import base64
import datetime
import json

from django.core.files.base import ContentFile
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated

from villa.api.serializer import *
from villa.models import *


@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def get_all_villas(request):
    all_villas = Villa.objects.all()
    serializer = VillaSerializer(all_villas, many=True)
    data = json.loads(json.dumps(serializer.data))
    return Response(data, status=status.HTTP_200_OK)
