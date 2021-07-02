import os

from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token

from account.models import Account

client = Client()

BASE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'tests')


class PushNotificationTest(TestCase):
    """ Test module for push notification """

    def setUp(self):
        new_user = Account.objects.create(
            first_name='Danial',
            last_name='Bazmandeh',
            email='danibazi9@gmail.com',
            phone_number='+989152147655',
            gender='Male',
            password='123456'
        )

        self.valid_token, self.created = Token.objects.get_or_create(user=new_user)
        self.invalid_token = 'fasdfs45dsfasd1fsfasdf4dfassf13'

        self.valid_push_notif = {
            'token': 'dfsfsdf@345hfdrfbgnntfgFhygvdrtnfdsf%5d4',
            'message': 'salaaaaaaam',
            'title': 'title'
        }

        self.invalid_push_notif = {
            'tok': 'dfsfsdf@345hfdrfbgnntfgFhygvdrtnfdsf%5d4',
        }

        self.invalid_push_notif2 = {
            'token': 'dfsfsdf@345hfdrfbgnntfgFhygvdrtnfdsf%5d4',
            'message': 'salaaaaaaam',
        }

        self.invalid_push_notif3 = {
            'tok': 'dfdghjmnbvcxs',
            'title': 'title'
        }

    def test_add_valid_villa(self):
        response = client.post(
            reverse('fcm-push-notification'),
            data=self.valid_push_notif,
            HTTP_AUTHORIZATION='Token {}'.format(self.valid_token),
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_add_invalid_villa(self):
        response = client.post(
            reverse('fcm-push-notification'),
            data=self.invalid_push_notif,
            HTTP_AUTHORIZATION='Token {}'.format(self.valid_token),
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = client.post(
            reverse('fcm-push-notification'),
            data=self.invalid_push_notif2,
            HTTP_AUTHORIZATION='Token {}'.format(self.valid_token),
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = client.post(
            reverse('fcm-push-notification'),
            data=self.invalid_push_notif3,
            HTTP_AUTHORIZATION='Token {}'.format(self.valid_token),
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_add_villa_unauthorized(self):
        response = client.post(
            reverse('fcm-push-notification'),
            data=self.valid_push_notif,
            HTTP_AUTHORIZATION='Token {}'.format(self.invalid_token),
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
