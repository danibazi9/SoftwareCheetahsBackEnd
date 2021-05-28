from push_notifications.models import GCMDevice
from rest_framework import status
from rest_framework.authtoken.models import Token
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

        fcm_device.send_message("This is a test notification",
                                title="New Notification")
    except Exception as e:
        return Response(f"ERROR: {e}", status=status.HTTP_400_BAD_REQUEST)

    return Response(f"Push notification successfully done!", status=status.HTTP_200_OK)
