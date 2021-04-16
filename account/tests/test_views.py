import json

from django.test import TestCase, Client

from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token

from account.models import Account

# initialize the APIClient app
client = Client()


class CheckExistenceTest(TestCase):
    """ Test module for check existence of a random account with email """

    def setUp(self):
        Account.objects.create(
            first_name='Danial',
            last_name='Bazmandeh',
            email='danibazi9@gmail.com',
            phone_number='+989152147655',
            gender='Male',
            password='123456'
        )

        self.valid_existence = {
            'email': 'danibazi9@gmail.com'
        }

        self.invalid_existence = {
            'email': 'dani@gmail.com'
        }

    def test_check_valid_existence(self):
        response = client.post(
            reverse('account:check-existence'),
            data=json.dumps(self.valid_existence),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_check_invalid_existence(self):
        response = client.post(
            reverse('account:check-existence'),
            data=json.dumps(self.invalid_existence),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class SignUpTest(TestCase):
    """ Test module for creating a new account """

    def setUp(self):
        self.valid_account = {
            'first_name': 'Ali',
            'last_name': 'Heydari',
            'email': 'ali_heydari@gmail.com',
            'phone_number': '+989152001235',
            'password': '123456',
            'vc_code': '000000'
        }

        self.invalid_account = {
            'first_name': 'Ali',
            'last_name': 'Heydari',
            'email': 'ali_heydari@gmail.com',
        }

    def test_create_valid_account(self):
        response = client.post(
            reverse('account:register'),
            data=json.dumps(self.valid_account),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_account(self):
        response = client.post(
            reverse('account:register'),
            data=json.dumps(self.invalid_account),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class LoginTest(TestCase):
    """ Test module for login a created account """

    def setUp(self):
        Account.objects.create_user(
            email='danibazi9@gmail.com',
            password='123456'
        )

        self.valid_login = {
            'username': 'danibazi9@gmail.com',
            'password': '123456'
        }

        self.invalid_login = {
            'username': 'danibazi9@gmail.com',
            'password': '1234'
        }

    def test_valid_login(self):
        response = client.post(
            reverse('account:login'),
            data=json.dumps(self.valid_login),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_login(self):
        response = client.post(
            reverse('account:login'),
            data=json.dumps(self.invalid_login),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class LogoutTest(TestCase):
    """ Test module for logout from a created account """

    def setUp(self):
        account = Account.objects.create(
            first_name='Danial',
            last_name='Bazmandeh',
            email='danibazi9@gmail.com',
            phone_number='+989152147655',
            gender='Male',
            password='123456'
        )

        self.valid_token, self.created = Token.objects.get_or_create(user=account)
        self.invalid_token = '7900b33a300eff557ebbe2d5261d00e2eaaac880'

    def test_valid_logout(self):
        response = client.post(
            reverse('account:logout'),
            HTTP_AUTHORIZATION='Token {}'.format(self.valid_token.key),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_logout(self):
        response = client.post(
            reverse('account:logout'),
            HTTP_AUTHORIZATION='Token {}'.format(self.invalid_token),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class EmailTest(TestCase):
    """ Test module for send email to a created account to verify """

    def setUp(self):
        self.valid_send_email = {
            'first_name': 'Ali',
            'email': 'ali_heydari@gmail.com'
        }

        self.invalid_send_email = {
            'first_name': 'Danial',
        }

    def test_valid_logout(self):
        response = client.post(
            reverse('account:send_email'),
            data=json.dumps(self.valid_send_email),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_logout(self):
        response = client.post(
            reverse('account:send_email'),
            data=json.dumps(self.invalid_send_email),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
class ProfilePictureTest(TestCase):
    def setUp(self):
        account = Account.objects.create(
            first_name='Danial',
            last_name='Bazmandeh',
            email='danibazi9@gmail.com',
            phone_number='+989152147655',
            gender='Male',
            password='123456'
        )

        self.valid_token, self.created = Token.objects.get_or_create(user=account)
        #self.invalid_token = '7900b33a300eff557ebbe2d5261d00e2eaaac880'

    def test_update_account_image(self):
        data = {'base64': 'test'}
        response = client.post(
            reverse('account:update_account_image'),
            data=json.dumps(data),
            HTTP_AUTHORIZATION='Token {}'.format(self.valid_token.key),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
