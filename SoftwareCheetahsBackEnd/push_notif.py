from push_notifications.models import GCMDevice
from rest_framework import status
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


@permission_classes((IsAuthenticated,))
@api_view(['POST', ])
def fcm_push_notifications(request):
    if 'token' not in request.data:
        return Response(f"Token: None, BAD REQUEST!", status=status.HTTP_400_BAD_REQUEST)

    token = request.data['token']

    try:
        fcm_device, created = GCMDevice.objects.get_or_create(registration_id=token,
                                                              cloud_message_type="FCM",
                                                              user=request.user)

        if 'message' not in request.data:
            return Response(f"Message: None, BAD REQUEST!", status=status.HTTP_400_BAD_REQUEST)

        if 'title' not in request.data:
            return Response(f"Title: None, BAD REQUEST!", status=status.HTTP_400_BAD_REQUEST)

        message = request.data['message']
        title = request.data['title']

        fcm_device.send_message(message=message, title=title)
    except Exception as e:
        return Response(f"ERROR: {e}", status=status.HTTP_400_BAD_REQUEST)

    return Response(f"Push notification successfully done!", status=status.HTTP_200_OK)


@permission_classes((IsAuthenticated,))
@api_view(['POST', ])
def fcm_add_device(request):
    if 'token' not in request.data:
        return Response(f"Token: None, BAD REQUEST!", status=status.HTTP_400_BAD_REQUEST)

    token = request.data['token']

    try:
        fcm_device = GCMDevice.objects.get(user=request.user)
        fcm_device.registration_id = token
        fcm_device.save()
    except GCMDevice.DoesNotExist:
        GCMDevice.objects.create(registration_id=token, cloud_message_type="FCM", user=request.user)

    return Response(f"FCM device info updated!", status=status.HTTP_200_OK)
