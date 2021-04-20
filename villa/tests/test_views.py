import json

from django.test import TestCase, Client

from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.conf import settings
import tempfile
from datetime import datetime, timedelta

from villa.models import Villa, Calendar
from account.models import Account

# initialize the APIClient app
client = Client()

class VillaSearchTest(TestCase):
    def setUp(self):
        owner = Account.objects.create(
            first_name='Danial',
            last_name='Bazmandeh',
            email='danibazi9@gmail.com',
            phone_number='+989152147655',
            gender='Male',
            password='123456'
        )

        Villa.objects.create(
            name='test1',
            type='Urban',
            price_per_night=10,
            country='Iran',
            city='Esfahan',
            address='Iran Esfahan',
            latitude=100,
            longitude=100,
            area=1,
            owner=owner,
            capacity=10
        )

        Villa.objects.create(
            name='test2',
            type='Urban',
            price_per_night=10,
            country='Iran',
            city='Tehran',
            address='Iran Tehran',
            latitude=100,
            longitude=100,
            area=1,
            owner=owner,
            capacity=10
        )

        Villa.objects.create(
            name='test3',
            type='Urban',
            price_per_night=10,
            country='Iran',
            city='Esfahan',
            address='Iran Esfahan',
            latitude=100,
            longitude=100,
            area=1,
            owner=owner,
            capacity=10
        )

    def test_search_villa(self):
        datas = [{'country':'Iran'},{'city':'Esfahan'},{'country':'Iran','city':'Tehran'}]
        result_count = [3,2,1]
        for test in range(len(result_count)):
            response = client.get(
                reverse('villa:search'),
                data = datas[test],
            )
            self.assertEquals(len(response.data['data']),result_count[test])

class CalendarTest(TestCase):
    def setUp(self):
        owner = Account.objects.create(
            first_name='Danial',
            last_name='Bazmandeh',
            email='danibazi9@gmail.com',
            phone_number='+989152147655',
            gender='Male',
            password='123456'
        )

        customer = Account.objects.create(
            first_name='Sadegh',
            last_name='Jafari',
            email='sadeghjafari@gmail.com',
            phone_number='+989152147655',
            gender='Male',
            password='123456'
        )

        v1 = Villa.objects.create(
            name='test1',
            type='Urban',
            price_per_night=10,
            country='Iran',
            city='Esfahan',
            address='Iran Esfahan',
            latitude=100,
            longitude=100,
            area=1,
            owner=owner,
            capacity=10
        )

        v2 = Villa.objects.create(
            name='test2',
            type='Urban',
            price_per_night=10,
            country='Iran',
            city='Tehran',
            address='Iran Tehran',
            latitude=100,
            longitude=100,
            area=1,
            owner=owner,
            capacity=10
        )

        Calendar.objects.create(
            customer=customer,
            villa=v1,
            start_date=datetime.now(),
            end_date=datetime.now() + timedelta(days=1)
        )

        Calendar.objects.create(
            customer=customer,
            villa=v1,
            start_date=datetime.now() + timedelta(days=3),
            end_date=datetime.now() + timedelta(days=5)
        )

        Calendar.objects.create(
            customer=customer,
            villa=v2,
            start_date=datetime.now() + timedelta(days=3),
            end_date=datetime.now() + timedelta(days=5)
        )

    def test_show_calendar(self):
        tests = [{'villa_id':1}, {'villa_id':2}]
        outputs = [2, 1]

        for test in tests:
            pass
