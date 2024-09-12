from chat.models import Chat, Message
import pytz

from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token

from django.conf import settings
import tempfile
from datetime import date, datetime, timedelta

from villa.models import *
from account.models import Account

client = Client()

class ShowChatsTest(TestCase):

    def setUp(self) -> None:
        user = Account.objects.create(
            first_name='Danial',
            last_name='Bazmandeh',
            email='danibazi9@gmail.com',
            phone_number='+989152147655',
            gender='Male',
            password='123456'
        )
        user.username = user.email
        user.save()

        self.valid_token, self.created = Token.objects.get_or_create(user=user)
        self.invalid_token = 'fasdfs45dsfasd1fsfasdf4dfassf13'

        contact = Account.objects.create(
            first_name='Sadegh',
            last_name='Jafari',
            email='sadeghjafari@gmail.com',
            phone_number='+989152147501',
            gender='Male',
            password='123456'
        )
        contact.username = contact.email
        contact.save()

        user2 = Account.objects.create(
            first_name='Saleh',
            last_name='Jafari',
            email='sadeghjafari5528@gmail.com',
            phone_number='+989152147500',
            gender='Male',
            password='123456'
        )
        user2.username = user2.email
        user2.save()

        self.valid_token2, self.created2 = Token.objects.get_or_create(user=user2)

        chat1 = Chat.objects.create(
            account1 = user,
            account2 = contact
        )

        chat2 = Chat.objects.create(
            account1 = user2,
            account2 = contact
        )

        Message.objects.create(
            chat=chat1,
            owner=user,
            text='hello',
            time=datetime.now(tz=pytz.timezone('UTC'))
        )

    def test_invalid_token(self):
        response = client.get(
            reverse('chat:show_chat'),
            HTTP_AUTHORIZATION='Token {}'.format(self.invalid_token),
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_with_last_message(self):
        response = client.get(
            reverse('chat:show_chat'),
            HTTP_AUTHORIZATION='Token {}'.format(self.valid_token),
        )

        data = response.data
        self.assertEqual('hello', data['data'][0]['last_message']['text'])

    def test_null_last_message(self):
        response = client.get(
            reverse('chat:show_chat'),
            HTTP_AUTHORIZATION='Token {}'.format(self.valid_token2),
        )

        data = response.data
        self.assertEqual(None, data['data'][0]['last_message'])


class AddChatTest(TestCase):

    def setUp(self) -> None:
        user = Account.objects.create(
            first_name='Danial',
            last_name='Bazmandeh',
            email='danibazi9@gmail.com',
            phone_number='+989152147655',
            gender='Male',
            password='123456'
        )
        user.username = user.email
        user.save()

        self.valid_token, self.created = Token.objects.get_or_create(user=user)
        self.invalid_token = 'fasdfs45dsfasd1fsfasdf4dfassf13'

        contact = Account.objects.create(
            first_name='Sadegh',
            last_name='Jafari',
            email='sadeghjafari@gmail.com',
            phone_number='+989152147501',
            gender='Male',
            password='123456'
        )
        contact.username = contact.email
        contact.save()

        contact2 = Account.objects.create(
            first_name='Saleh',
            last_name='Jafari',
            email='sadeghjafari5528@gmail.com',
            phone_number='+989152147500',
            gender='Male',
            password='123456'
        )
        contact2.username = contact2.email
        contact2.save()

        chat2 = Chat.objects.create(
            account1 = user,
            account2 = contact2
        )

    def test_invalid_token(self):
        response = client.post(
            reverse('chat:add_chat'),
            HTTP_AUTHORIZATION='Token {}'.format(self.invalid_token),
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_invalid_request_body(self):
        response = client.post(
            reverse('chat:add_chat'),
            HTTP_AUTHORIZATION='Token {}'.format(self.valid_token),
            data = {}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_contact_does_not_exist(self):
        response = client.post(
            reverse('chat:add_chat'),
            HTTP_AUTHORIZATION='Token {}'.format(self.valid_token),
            data = {'contact':5}
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_and_contact_is_equal(self):
        response = client.post(
            reverse('chat:add_chat'),
            HTTP_AUTHORIZATION='Token {}'.format(self.valid_token),
            data = {'contact':1}
        )
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)

    def test_chat_is_already_exist(self):
        response = client.post(
            reverse('chat:add_chat'),
            HTTP_AUTHORIZATION='Token {}'.format(self.valid_token),
            data = {'contact':3}
        )
        self.assertEqual(response.status_code, status.HTTP_208_ALREADY_REPORTED)

    def test_create_new_chat(self):
        response = client.post(
            reverse('chat:add_chat'),
            HTTP_AUTHORIZATION='Token {}'.format(self.valid_token),
            data = {'contact':2}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

