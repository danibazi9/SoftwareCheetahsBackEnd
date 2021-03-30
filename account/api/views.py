import base64
import json

from django.core.files.base import ContentFile
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from account.api.serializer import *
from validate_email import validate_email
from account.models import Account
from rest_framework.views import APIView
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
import random


@api_view(['POST'])
def registration_view(request):
    serializer = RegistrationSerializer(data=request.data)
    data = {}
    if serializer.is_valid():
        if validate_email(serializer.validated_data.get('email')):
            account = serializer.save()

            if 'filename' in request.data and 'image' in request.data:
                filename = request.data['filename']
                file = ContentFile(base64.b64decode(request.data['image']), name=filename)
                account.image = file

            account.save()

            data['response'] = 'successful'
            token = Token.objects.get(user=account).key
            data['token'] = token

            serializer = AccountPropertiesSerializer(account)
            info = json.loads(json.dumps(serializer.data))

            for key in info:
                data[key] = info[key]

            return Response(data=data, status=status.HTTP_201_CREATED)
        else:
            return Response(f"The email '{serializer['email'].value}' doesn't exist",
                            status=status.HTTP_406_NOT_ACCEPTABLE)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', ])
def account_properties_view(request):
    try:
        account = request.user
    except Account.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = AccountPropertiesSerializer(account)
        return Response(serializer.data)


@api_view(('GET',))
def all_accounts_view(request):
    all_accounts = Account.objects.all()

    if request.method == 'GET':
        serializer = AccountPropertiesSerializer(all_accounts, many=True)
        return Response(serializer.data)


class TokenObtainView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        custom_response = {'token': token.key}

        user_to_login = Account.objects.get(email=request.data['username'])
        serializer = AccountPropertiesSerializer(user_to_login)
        info = json.loads(json.dumps(serializer.data))

        for key in info:
            custom_response[key] = info[key]

        return Response(custom_response, status=status.HTTP_200_OK)


@permission_classes((IsAuthenticated,))
class logoutView(APIView):
    def post(self, request):
        # simply delete the token to force a login
        request.user.auth_token.delete()
        return Response("Successfully logged out!", status=status.HTTP_200_OK)


@api_view(['POST', ])
@permission_classes((IsAuthenticated,))
def update_account_view(request):
    account = request.user

    data = request.data

    file = ""
    if 'filename' in data and 'image' in data:
        filename = data['filename']
        file = ContentFile(base64.b64decode(data['image']), name=filename)

    account.first_name = data['first_name']
    account.last_name = data['last_name']
    account.image = file
    account.phone_number = data['phone_number']

    if 'gender' in data:
        gender = data['gender']
        if gender == 'Male' or gender == 'Female':
            account.gender = gender
        else:
            return Response("Gender: Not Acceptable!", status=status.HTTP_406_NOT_ACCEPTABLE)

    if 'bio' in request.data:
        account.bio = data['bio']

    if 'national_code' in request.data:
        national_code = data['national_code']
        if len(national_code) > 10:
            return Response("National Code: Not Acceptable!", status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            account.national_code = national_code

    account.save()

    my_serializer = AccountPropertiesSerializer(account)
    data = json.loads(json.dumps(my_serializer.data))

    return Response(data, status=status.HTTP_205_RESET_CONTENT)


@permission_classes((IsAuthenticated,))
class SendEmail(APIView):
    def get(self, request):
        user_to_send_email = self.request.user

        random_code_generated = random.randrange(100000, 999999)

        template = render_to_string('account/email_template.html',
                                    {'name': user_to_send_email.first_name,
                                     'code': random_code_generated})

        email = EmailMessage(
            'Welcome to MyUniversity Platform!',
            template,
            'MyUniversity Organization',
            [user_to_send_email.email]
        )

        email.content_subtype = "html"
        email.fail_silently = False
        email.send()

        serializer = AccountPropertiesSerializer(user_to_send_email)
        json_response = {"email": serializer.data['email'], "vc_code": random_code_generated}
        return Response(json_response)


@api_view(['POST' , ])
def checkUniqueness(request):
    if request.method == 'POST':
        data = dict(request.POST)
        errors = {}
        if 'username' in data.keys():
            if list(Account.objects.filter(username=data['username'][0])) != []:
                errors['username'] = 'This username already exist'
        if 'email' in data.keys():
            if list(Account.objects.filter(email=data['email'][0])) != []:
                errors['email'] = 'This email already exist'
        if 'phone' in data.keys():
            if list(Account.objects.filter(phone=data['phone'][0])) != []:
                errors['phone'] = 'This phone already exist'
        return Response({'errors' : errors})     
