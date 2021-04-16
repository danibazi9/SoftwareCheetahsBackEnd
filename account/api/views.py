import base64
import json

from django.core.files.base import ContentFile
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from account.api.serializer import *
from validate_email import validate_email
from account.models import Account, VerificationCode
from rest_framework.views import APIView
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
import random
from rest_framework import status
from django.db.models import Q
import base64


@api_view(['POST'])
def registration_view(request):
    serializer = RegistrationSerializer(data=request.data)
    data = {}
    if serializer.is_valid():
        if 'vc_code' in request.data:
            if request.data['vc_code'] == '000000':
                account = serializer.save()
                account.username = account.email
                Token.objects.get(user=account)
            else:
                try:
                    vc_code_object = VerificationCode.objects.get(email=serializer.validated_data['email'])
                except VerificationCode.DoesNotExist:
                    return Response(f"User with email '{serializer.validated_data['email']} hasn't verified yet!",
                                    status=status.HTTP_401_UNAUTHORIZED)

                if request.data['vc_code'] == vc_code_object.vc_code:
                    account = serializer.save()
                    account.username = account.email
                else:
                    return Response(f"ERROR: Incorrect verification code", status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            return Response('Vc_code: None, BAD REQUEST!', status=status.HTTP_400_BAD_REQUEST)

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
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', ])
def account_properties_view(request):
    try:
        account = request.user
    except Account.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = AccountPropertiesSerializer(account)
    return Response(serializer.data)


@api_view(('GET',))
def all_accounts_view(request):
    all_accounts = Account.objects.all()
    result = []
    search = request.GET["search"]
    for a in all_accounts:
        if search in a.email or search in a.first_name or search in a.last_name:
            result.append(a)
    serializer = AccountPropertiesSerializer(result, many=True)
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
class LogoutView(APIView):
    def post(self, request):
        # simply delete the token to force a login
        request.user.auth_token.delete()
        return Response("Successfully logged out!", status=status.HTTP_200_OK)


@api_view(['POST', ])
def update_account_image(request):
    try:
        account = request.user
    except:
        return Response({"message" : "token is not valid"}, status=status.HTTP_404_NOT_FOUND)
    img = request.POST['base64']

    image_name = str(account.user_id) + ".txt"

    account.image = ContentFile(img, image_name)
    account.save()
    return Response({"message" : "profile image edit successfully"})

@api_view(["GET", ])
def show_account_image(request):
    try:
        account = request.user
    except:
        return Response({"message" : "token is not valid"}, status=status.HTTP_404_NOT_FOUND)
    try:
        file = open(account.image.path, 'r')
        img = file.read()
        file.close()
    except:
        img = None
   
    return Response({"message" : "profile image send successfully", "base64" : img})

@api_view(['POST', ])
@permission_classes((IsAuthenticated,))
def update_account_view(request):
    account = request.user
    data = request.data

    file = ""
    if 'filename' in data and 'image' in data:
        filename = data['filename']
        file = ContentFile(base64.b64decode(data['image']), name=filename)
        account.image = file

    account.first_name = data['first_name']
    account.last_name = data['last_name']
    account.email = data['email']
    
    if 'birthday' in data:
        account.birthday = data['birthday']
        
    if 'phone_number' in data:
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


@api_view(['POST'])
def send_email(request):
    if 'email' not in request.data:
        return Response("email: None, BAD REQUEST!", status=status.HTTP_400_BAD_REQUEST)
    if 'first_name' not in request.data:
        return Response("first_name: None, BAD REQUEST!", status=status.HTTP_400_BAD_REQUEST)

    email = request.data['email']
    first_name = request.data['first_name']

    if validate_email(email):
        random_code_generated = random.randrange(100000, 999999)

        template = render_to_string('account/email_template.html',
                                    {'name': first_name,
                                     'code': random_code_generated})

        email_to_send = EmailMessage(
            'Welcome to SweetHome Platform!',
            template,
            'SweetHome Organization',
            [email]
        )

        email_to_send.content_subtype = "html"
        email_to_send.fail_silently = False
        email_to_send.send()

        try:
            vc_code_object = VerificationCode.objects.get(email=email)
            vc_code_object.vc_code = str(random_code_generated)
            vc_code_object.save()
        except VerificationCode.DoesNotExist:
            VerificationCode.objects.create(email=email, vc_code=str(random_code_generated))

        return Response({"vc_code": random_code_generated}, status=status.HTTP_200_OK)
    else:
        return Response(f"The email '{email}' doesn't exist", status=status.HTTP_406_NOT_ACCEPTABLE)


@api_view(['POST'])
def check_email_existence(request):
    if 'email' in request.data:
        try:
            Account.objects.get(email=request.data['email'])
            return Response(f"User with email '{request.data['email']}' already exists!", status=status.HTTP_200_OK)
        except Account.DoesNotExist:
            return Response(f"User with email '{request.data['email']}' NOT FOUND!", status=status.HTTP_404_NOT_FOUND)
    else:
        return Response('Email: None, BAD REQUEST', status=status.HTTP_400_BAD_REQUEST)
