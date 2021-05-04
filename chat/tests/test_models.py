from unittest import mock

from django.core.files import File
from django.test import TestCase
from datetime import datetime
import pytz

from account.models import Account
from chat.models import Chat, Message


class ChatTest(TestCase):
    """ Test module for Account model """

    def setUp(self):
        self.account1 = Account.objects.create(
            first_name='Danial',
            last_name='Bazmandeh',
            email='danibazi9@gmail.com',
            phone_number='+989152147655',
            gender='Male',
            password='123456'
        )

        self.account2 = Account.objects.create(
            first_name='Sadegh',
            last_name='Jafari',
            email='sadeghjafari5528@gmail.com',
            phone_number='+989140387851',
            gender='Male',
            password='123456'
        )

        self.chat = Chat.objects.create(
            account1=self.account1,
            account2=self.account2
        )

    def test_account1_id(self):
        chat = Chat.objects.get(chat_id=self.chat.chat_id)
        self.assertEqual(chat.account1.user_id, self.account1.user_id)

    def test_account2_id(self):
        chat = Chat.objects.get(chat_id=self.chat.chat_id)
        self.assertEqual(chat.account2.user_id, self.account2.user_id)


class MessageTest(TestCase):
    """ Test module for Account model """

    def setUp(self):
        self.account1 = Account.objects.create(
            first_name='Danial',
            last_name='Bazmandeh',
            email='danibazi9@gmail.com',
            phone_number='+989152147655',
            gender='Male',
            password='123456'
        )

        self.account2 = Account.objects.create(
            first_name='Sadegh',
            last_name='Jafari',
            email='sadeghjafari5528@gmail.com',
            phone_number='+989140387851',
            gender='Male',
            password='123456'
        )

        self.chat = Chat.objects.create(
            account1=self.account1,
            account2=self.account2
        )

        self.time = datetime.now(tz=pytz.timezone('UTC'))

        self.message = Message.objects.create(
            chat=self.chat,
            owner=self.account1,
            text="hello Sadegh",
            parentMessage=None,
            time=self.time
        )

    def test_chat_id(self):
        message = Message.objects.get(message_id=self.message.message_id)
        self.assertEqual(message.chat.chat_id, self.chat.chat_id)

    def test_owner_id(self):
        message = Message.objects.get(message_id=self.message.message_id)
        self.assertEqual(message.owner.user_id, self.account1.user_id)

    def test_text(self):
        message = Message.objects.get(message_id=self.message.message_id)
        self.assertEqual(message.text, "hello Sadegh")

    def test_parentMessage(self):
        message = Message.objects.get(message_id=self.message.message_id)
        self.assertEqual(message.parentMessage, None)

    def test_time(self):
        message = Message.objects.get(message_id=self.message.message_id)
        self.assertEqual(message.time, self.time)