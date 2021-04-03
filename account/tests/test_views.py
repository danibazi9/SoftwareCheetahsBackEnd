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
