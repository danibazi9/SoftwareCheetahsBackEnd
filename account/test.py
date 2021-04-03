import json

from django.test import TestCase, Client

from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token

from account.models import Account

client = Client()


class ProfileTest(TestCase):

    def setUp(self):
        account = Account.objects.create(
            first_name='sadegh',
            last_name='jafari',
            email='sadegh@gmail.com',
            phone_number='+989140387851',
            gender='Male',
            password='1'
        )

        self.valid_token, self.created = Token.objects.get_or_create(user=account)


    def test_show_properties(self):
        response = client.get(
            reverse('account:properties'),
            HTTP_AUTHORIZATION='Token {}'.format(self.valid_token.key),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_account_view(self):
        data = {'first_name': 'test','last_name': 'test2', 'email': 'test@test.com'}
        response = client.post(
            reverse('account:update'),
            data=json.dumps(data),
            HTTP_AUTHORIZATION='Token {}'.format(self.valid_token.key),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_205_RESET_CONTENT)

    def test_all_accounts_view(self):
        data = {'search': 's'}
        response = client.get(
            reverse('account:properties_all'),
            data=data,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)        
