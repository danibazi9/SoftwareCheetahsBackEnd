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


