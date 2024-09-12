import os
import json

from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token

from django.conf import settings
import tempfile
from datetime import datetime, timedelta

from villa.models import *
from account.models import Account

client = Client()

BASE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'tests')


class CheckGetAllVillas(TestCase):
    """ Test module for get all villas that user owns """

    def setUp(self):
        new_user = Account.objects.create(
            first_name='Danial',
            last_name='Bazmandeh',
            email='danibazi9@gmail.com',
            phone_number='+989152147655',
            gender='Male',
            password='123456'
        )

        Villa.objects.create(
            name='My Villaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa3453342@$%@$%^^56#7865xcvxcvxv2345665DFSDFDSasdasd4',
            type='Coastal',
            price_per_night=3456765432234567,
            country='Irannnnsdfthg3$%#@#',
            state='Mazandaran',
            city='Sari',
            address='St 2.',
            postal_code='9738920343',
            latitude=0,
            longitude=0,
            area=15200,
            owner=new_user,
            capacity=10,
            max_capacity=15,
            number_of_bathrooms=234564324,
            number_of_bedrooms=2344534,
            number_of_single_beds=2343454,
            number_of_double_beds=14444,
            number_of_showers=4452
        )

        self.valid_token, self.created = Token.objects.get_or_create(user=new_user)

        self.invalid_token = 'fasdfs45dsfasd1fsfasdf4dfassf13'

    def test_get_all_villas_authorized(self):
        response = client.get(
            reverse('villa:get_all_villas'),
            HTTP_AUTHORIZATION='Token {}'.format(self.valid_token.key),
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_villas_unauthorized(self):
        response = client.get(
            reverse('villa:get_all_villas'),
            HTTP_AUTHORIZATION='Token {}'.format(self.invalid_token),
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class UploadImageTest(TestCase):
    """ Test module for uploading a new image in database """

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

        valid_image = open(os.path.join(BASE_DIR, 'danial.jpg'), 'rb')
        invalid_image = open(os.path.join(BASE_DIR, 'file.pdf'), 'rb')

        self.valid_upload = {
            'file': valid_image
        }

        self.invalid_upload = {
        }

        self.invalid_upload2 = {
            'imageddf32': valid_image
        }

        self.invalid_upload3 = {
            'file': invalid_image
        }

    def test_upload_valid_image(self):
        response = client.post(
            reverse('villa:upload_image'),
            data=self.valid_upload,
            HTTP_AUTHORIZATION='Token {}'.format(self.valid_token),
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_upload_invalid_image(self):
        response = client.post(
            reverse('villa:upload_image'),
            data=self.invalid_upload,
            HTTP_AUTHORIZATION='Token {}'.format(self.valid_token),
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = client.post(
            reverse('villa:upload_image'),
            data=self.invalid_upload2,
            HTTP_AUTHORIZATION='Token {}'.format(self.valid_token),
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = client.post(
            reverse('villa:upload_image'),
            data=self.invalid_upload3,
            HTTP_AUTHORIZATION='Token {}'.format(self.valid_token),
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_upload__image_unauthorized(self):
        response = client.post(
            reverse('villa:upload_image'),
            data=self.valid_upload,
            HTTP_AUTHORIZATION='Token {}'.format(self.invalid_token),
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class UploadDocumentTest(TestCase):
    """ Test module for uploading a new document for villa in database """

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

        document = open(os.path.join(BASE_DIR, 'file.pdf'), 'rb')

        self.valid_upload = {
            'file': document
        }

        self.invalid_upload = {
        }

        self.invalid_upload2 = {
            'image': document
        }

    def test_upload_valid_document(self):
        response = client.post(
            reverse('villa:upload_document'),
            data=self.valid_upload,
            HTTP_AUTHORIZATION='Token {}'.format(self.valid_token),
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_upload_invalid_document(self):
        response = client.post(
            reverse('villa:upload_document'),
            data=self.invalid_upload,
            HTTP_AUTHORIZATION='Token {}'.format(self.valid_token),
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = client.post(
            reverse('villa:upload_document'),
            data=self.invalid_upload2,
            HTTP_AUTHORIZATION='Token {}'.format(self.valid_token),
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_upload__document_unauthorized(self):
        response = client.post(
            reverse('villa:upload_document'),
            data=self.valid_upload,
            HTTP_AUTHORIZATION='Token {}'.format(self.invalid_token),
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AddVillaTest(TestCase):
    """ Test module for adding a new villa in database """

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

        self.valid_villa = {
            'name': 'My Villaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa3453342@$%@$%^^56#7865xcvxcvxv2345665DFSDFDSasdasd4',
            'type': 'Coastal',
            'price_per_night': 3456765432234567,
            'country': 'Irannnnsdfthg3$%#@#',
            'state': 'Mazandaran',
            'city': 'Sari',
            'address': 'St 2.',
            'postal_code': '1234567890',
            'latitude': 1250.522,
            'longitude': 4855.785,
            'facilities_list': [
                'Washer',
                'Heater'
            ],
            'area': 15200,
            'owner': new_user,
            'capacity': 10,
            'max_capacity': 15,
            'number_of_bathrooms': 234564324,
            'number_of_bedrooms': 2344534,
            'number_of_single_beds': 2343454,
            'number_of_double_beds': 14444,
            'number_of_showers': 4452
        }

        self.invalid_villa = {
            'name': 'My dfsgjet5@$%@$%^^56#7865xcvxcvxv2345665DFSDFDSasdasd4',
            'type': 'Coastal',
        }

        # self.invalid_upload2 = {
        #     'image': document
        # }

    # def test_add_valid_villa(self):
    #     response = client.post(
    #         reverse('villa:villa_apis'),
    #         data=self.valid_villa,
    #         HTTP_AUTHORIZATION='Token {}'.format(self.valid_token),
    #     )
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_add_invalid_villa(self):
        response = client.post(
            reverse('villa:villa_apis'),
            data=self.invalid_villa,
            HTTP_AUTHORIZATION='Token {}'.format(self.valid_token),
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # response = client.post(
        #     reverse('villa:upload_document'),
        #     data=self.invalid_upload2,
        #     HTTP_AUTHORIZATION='Token {}'.format(self.valid_token),
        # )
        # self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_add_villa_unauthorized(self):
        response = client.post(
            reverse('villa:villa_apis'),
            data=self.valid_villa,
            HTTP_AUTHORIZATION='Token {}'.format(self.invalid_token),
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class GetFixedRulesTest(TestCase):
    """ Test module for get the list of fixed rules in database """

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

    def test_valid_get_fixed_rules(self):
        response = client.get(
            reverse('villa:get_fixed_rules'),
            HTTP_AUTHORIZATION='Token {}'.format(self.valid_token),
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_fixed_rules_unauthorized(self):
        response = client.get(
            reverse('villa:get_fixed_rules'),
            HTTP_AUTHORIZATION='Token {}'.format(self.invalid_token),
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class GetSpecialRulesTest(TestCase):
    """ Test module for get special rules in database """

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

    def test_valid_get_special_rules(self):
        response = client.get(
            reverse('villa:get_special_rules'),
            HTTP_AUTHORIZATION='Token {}'.format(self.valid_token),
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_special_rules_unauthorized(self):
        response = client.get(
            reverse('villa:get_special_rules'),
            HTTP_AUTHORIZATION='Token {}'.format(self.invalid_token),
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


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
        owner.username = owner.email
        owner.save()

        customer = Account.objects.create(
            first_name='Sadegh',
            last_name='Jafari',
            email='sadeghjafari@gmail.com',
            phone_number='+989152147501',
            gender='Male',
            password='123456'
        )
        customer.username = customer.email
        customer.save()

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
            capacity=10,
            max_capacity=10,
            postal_code='1234567890'
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
            capacity=10,
            max_capacity=16,
            postal_code='0123456789'
        )

        Calendar.objects.create(
            customer=customer,
            villa=v1,
            start_date=datetime.now(),
            end_date=datetime.now() + timedelta(days=1),
            num_of_passengers=10,
            total_cost=20001.25
        )

        Calendar.objects.create(
            customer=customer,
            villa=v1,
            start_date=datetime.now() + timedelta(days=3),
            end_date=datetime.now() + timedelta(days=5),
            num_of_passengers=4,
            total_cost=55677.4
        )

        Calendar.objects.create(
            customer=customer,
            villa=v2,
            start_date=datetime.now() + timedelta(days=3),
            end_date=datetime.now() + timedelta(days=5),
            num_of_passengers=13,
            total_cost=1004455.25
        )

    def test_search_villa(self):
        datas = [{'country': 'Iran', 'number_of_villa': 2, 'page': 1},
                 {'city': 'Esfahan', 'number_of_villa': 2, 'page': 1},
                 {'country': 'Iran', 'city': 'Tehran', 'number_of_villa': 2, 'page': 1}]

        result_count = [2, 1, 1]
        for test in range(len(result_count)):
            response = client.get(
                reverse('villa:search'),
                data=datas[test],
            )
            self.assertEquals(len(response.data['data']), result_count[test])

    def test_searchVilla_withDate(self):
        datas = [
            {'country': 'Iran', 'number_of_villa': 2, 'page': 1},
            {'city': 'Esfahan', 'number_of_villa': 2, 'page': 1},
            {'country': 'Iran', 'city': 'Tehran', 'number_of_villa': 2, 'page': 1}
        ]

        result_count = [2, 1, 1]

        for test in range(len(result_count)):
            response = client.get(
                reverse('villa:search'),
                data=datas[test],
            )
            self.assertEquals(len(response.data['data']), result_count[test])


class CalendarTest(TestCase):
    def setUp(self):
        new_user = Account.objects.create(
            first_name='Danial',
            last_name='Bazmandeh',
            email='danibazi@gmail.com',
            phone_number='+989152147654',
            gender='Male',
            password='123456'
        )
        new_user.username = new_user.email
        new_user.save()

        self.valid_token, self.created = Token.objects.get_or_create(user=new_user)
        self.invalid_token = 'fasdfs45dsfasd1fsfasdf4dfassf13'

        owner = Account.objects.create(
            first_name='Danial',
            last_name='Bazmandeh',
            email='danibazi9@gmail.com',
            phone_number='+989152147655',
            gender='Male',
            password='123456'
        )
        owner.username = owner.email
        owner.save()

        customer = Account.objects.create(
            first_name='Sadegh',
            last_name='Jafari',
            email='sadeghjafari@gmail.com',
            phone_number='+989152147501',
            gender='Male',
            password='123456'
        )
        customer.username = customer.email
        customer.save()

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
            capacity=10,
            max_capacity=20,
            postal_code='1234'
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
            capacity=10,
            max_capacity=20,
            postal_code='1235'
        )

        Calendar.objects.create(
            customer=customer,
            villa=v1,
            start_date=datetime.now(),
            end_date=datetime.now() + timedelta(days=1),
            num_of_passengers=10,
            total_cost=50,
            rate=3
        )

        Calendar.objects.create(
            customer=customer,
            villa=v1,
            start_date=datetime.now() + timedelta(days=3),
            end_date=datetime.now() + timedelta(days=5),
            num_of_passengers=10,
            total_cost=50,
            rate=3
        )

        Calendar.objects.create(
            customer=customer,
            villa=v2,
            start_date=datetime.now() + timedelta(days=3),
            end_date=datetime.now() + timedelta(days=5),
            num_of_passengers=10,
            total_cost=50,
            rate=3
        )

    def test_show_calendar(self):
        tests = [{'villa_id': 1}, {'villa_id': 2}]
        outputs = [5, 3]

        for test in range(len(tests)):
            responce = client.get(
                reverse("villa:show_calendar"),
                data=tests[test],
                HTTP_AUTHORIZATION='Token {}'.format(self.valid_token)
            )
            self.assertEquals(len(responce.data['dates']), outputs[test])

    def test_invalid_show_calendar(self):
        responce = client.get(
            reverse("villa:show_calendar"),
            data={"villa_id": 5},
            HTTP_AUTHORIZATION='Token {}'.format(self.valid_token)
        )
        self.assertEquals(responce.status_code, status.HTTP_404_NOT_FOUND)

    def test_invalid_token(self):
        response = client.get(
            reverse('villa:show_most_popular_city'),
            HTTP_AUTHORIZATION='Token {}'.format(self.invalid_token),
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class RegisterVillaTest(TestCase):
    """ Test module for registering a villa by user """

    def setUp(self):
        self.new_user = Account.objects.create(
            first_name='Danial',
            last_name='Bazmandeh',
            email='danibazi9@gmail.com',
            phone_number='+989152147655',
            gender='Male',
            password='123456'
        )

        self.new_villa = Villa.objects.create(
            name='test',
            type='Urban',
            price_per_night=10,
            country='Iran',
            city='Tehran',
            address='Iran Tehran',
            latitude=100,
            longitude=100,
            area=1,
            owner=self.new_user,
            capacity=10,
            max_capacity=16
        )

        self.valid_token, self.created = Token.objects.get_or_create(user=self.new_user)
        self.invalid_token = 'fasdfs45dsfasd1fsfasdf4dfassf13'

        self.valid_register_villa = {
            'villa': self.new_villa.villa_id,
            'start_date': datetime.strftime(datetime.now() + timedelta(days=3), '%Y-%m-%d'),
            'end_date': datetime.strftime(datetime.now() + timedelta(days=6), '%Y-%m-%d'),
            'num_of_passengers': 10,
            'total_cost': 20000.5
        }

        self.invalid_register_villa = {
            'villa': self.new_villa.villa_id,
        }

        self.invalid_register_villa2 = {
            'villa': self.new_villa.villa_id,
            'start_date': datetime.strftime(datetime.now() + timedelta(days=6), '%Y-%m-%d'),
            'end_date': datetime.strftime(datetime.now() + timedelta(days=3), '%Y-%m-%d'),
        }

        self.invalid_register_villa3 = {
            'villa': self.new_villa.villa_id,
            'start_date': datetime.strftime(datetime.now() - timedelta(days=6), '%Y-%m-%d'),
            'end_date': datetime.strftime(datetime.now() + timedelta(days=3), '%Y-%m-%d'),
        }

        self.invalid_register_villa4 = {
            'villa': self.new_villa.villa_id,
            'start_date': datetime.strftime(datetime.now() - timedelta(days=6), '%Y-%m-%d'),
            'end_date': datetime.strftime(datetime.now() - timedelta(days=3), '%Y-%m-%d'),
        }

        self.invalid_register_villa5 = {
            'villa': self.new_villa.villa_id,
            'start_date': datetime.strftime(datetime.now() + timedelta(days=1), '%Y-%m-%d'),
            'end_date': datetime.strftime(datetime.now() + timedelta(days=5), '%Y-%m-%d'),
        }

        self.invalid_register_villa6 = {
            'villa': self.new_villa.villa_id,
            'start_date': datetime.strftime(datetime.now() + timedelta(days=1), '%Y-%m-%d'),
            'end_date': datetime.strftime(datetime.now() + timedelta(days=8), '%Y-%m-%d'),
        }

        self.invalid_register_villa7 = {
            'villa': self.new_villa.villa_id,
            'start_date': datetime.strftime(datetime.now() + timedelta(days=4), '%Y-%m-%d'),
            'end_date': datetime.strftime(datetime.now() + timedelta(days=8), '%Y-%m-%d'),
        }

        self.invalid_register_villa8 = {
            'villa': self.new_villa.villa_id,
            'start_date': datetime.strftime(datetime.now() + timedelta(days=4), '%Y-%m-%d'),
            'end_date': datetime.strftime(datetime.now() + timedelta(days=6), '%Y-%m-%d'),
        }

    def test_valid_register_villa(self):
        response = client.post(
            reverse('villa:register_villa'),
            data=self.valid_register_villa,
            HTTP_AUTHORIZATION='Token {}'.format(self.valid_token),
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_invalid_register_villa(self):
        response = client.post(
            reverse('villa:register_villa'),
            data=self.invalid_register_villa,
            HTTP_AUTHORIZATION='Token {}'.format(self.valid_token),
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = client.post(
            reverse('villa:register_villa'),
            data=self.invalid_register_villa2,
            HTTP_AUTHORIZATION='Token {}'.format(self.valid_token),
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = client.post(
            reverse('villa:register_villa'),
            data=self.invalid_register_villa3,
            HTTP_AUTHORIZATION='Token {}'.format(self.valid_token),
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = client.post(
            reverse('villa:register_villa'),
            data=self.invalid_register_villa4,
            HTTP_AUTHORIZATION='Token {}'.format(self.valid_token),
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        Calendar.objects.create(
            customer=self.new_user,
            villa=self.new_villa,
            start_date=datetime.now() + timedelta(days=3),
            end_date=datetime.now() + timedelta(days=6),
            num_of_passengers=10,
            total_cost=10222.02
        )

        response = client.post(
            reverse('villa:register_villa'),
            data=self.invalid_register_villa5,
            HTTP_AUTHORIZATION='Token {}'.format(self.valid_token),
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = client.post(
            reverse('villa:register_villa'),
            data=self.invalid_register_villa6,
            HTTP_AUTHORIZATION='Token {}'.format(self.valid_token),
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = client.post(
            reverse('villa:register_villa'),
            data=self.invalid_register_villa7,
            HTTP_AUTHORIZATION='Token {}'.format(self.valid_token),
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = client.post(
            reverse('villa:register_villa'),
            data=self.invalid_register_villa8,
            HTTP_AUTHORIZATION='Token {}'.format(self.valid_token),
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_villa_unauthorized(self):
        response = client.post(
            reverse('villa:register_villa'),
            data=self.valid_register_villa,
            HTTP_AUTHORIZATION='Token {}'.format(self.invalid_token),
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class MostPopularCityTest(TestCase):
    def setUp(self) -> None:
        new_user = Account.objects.create(
            first_name='Danial',
            last_name='Bazmandeh',
            email='danibazi@gmail.com',
            phone_number='+989152147654',
            gender='Male',
            password='123456'
        )
        new_user.username = new_user.email
        new_user.save()

        self.valid_token, self.created = Token.objects.get_or_create(user=new_user)
        self.invalid_token = 'fasdfs45dsfasd1fsfasdf4dfassf13'

        owner = Account.objects.create(
            first_name='Danial',
            last_name='Bazmandeh',
            email='danibazi9@gmail.com',
            phone_number='+989152147655',
            gender='Male',
            password='123456'
        )
        owner.username = owner.email
        owner.save()

        customer = Account.objects.create(
            first_name='Sadegh',
            last_name='Jafari',
            email='sadeghjafari@gmail.com',
            phone_number='+989152147501',
            gender='Male',
            password='123456'
        )
        customer.username = customer.email
        customer.save()

        v1 = Villa.objects.create(
            name='test1',
            type='Urban',
            price_per_night=10,
            country='Iran',
            state='Esfahan',
            city='Esfahan',
            address='Iran Esfahan',
            latitude=100,
            longitude=100,
            area=1,
            owner=owner,
            capacity=10,
            max_capacity=20,
            postal_code='1234'
        )

        v2 = Villa.objects.create(
            name='test2',
            type='Urban',
            price_per_night=10,
            country='Iran',
            state='Tehran',
            city='Tehran',
            address='Iran Tehran',
            latitude=100,
            longitude=100,
            area=1,
            owner=owner,
            capacity=10,
            max_capacity=20,
            postal_code='1235'
        )

        v3 = Villa.objects.create(
            name='test3',
            type='Urban',
            price_per_night=10,
            country='Iran',
            state='Esfahan',
            city='Esfahan',
            address='Iran Esfahan',
            latitude=100,
            longitude=100,
            area=1,
            owner=owner,
            capacity=10,
            max_capacity=20,
            postal_code='123445'
        )

        Calendar.objects.create(
            customer=customer,
            villa=v1,
            start_date=datetime.now(),
            end_date=datetime.now() + timedelta(days=1),
            num_of_passengers=10,
            total_cost=50,
            rate=3
        )

        Calendar.objects.create(
            customer=customer,
            villa=v1,
            start_date=datetime.now() + timedelta(days=3),
            end_date=datetime.now() + timedelta(days=5),
            num_of_passengers=5,
            total_cost=40
        )

        Calendar.objects.create(
            customer=customer,
            villa=v3,
            start_date=datetime.now(),
            end_date=datetime.now() + timedelta(days=1),
            num_of_passengers=10,
            total_cost=50,
            rate=3
        )

        Calendar.objects.create(
            customer=customer,
            villa=v3,
            start_date=datetime.now() + timedelta(days=3),
            end_date=datetime.now() + timedelta(days=5),
            num_of_passengers=5,
            total_cost=40
        )

        Calendar.objects.create(
            customer=customer,
            villa=v2,
            start_date=datetime.now() + timedelta(days=3),
            end_date=datetime.now() + timedelta(days=5),
            num_of_passengers=4,
            total_cost=100,
            rate=1
        )

        Calendar.objects.create(
            customer=customer,
            villa=v2,
            start_date=datetime.now() + timedelta(days=3),
            end_date=datetime.now() + timedelta(days=5),
            num_of_passengers=5,
            total_cost=40,
            rate=5
        )

        Calendar.objects.create(
            customer=customer,
            villa=v2,
            start_date=datetime.now() + timedelta(days=3),
            end_date=datetime.now() + timedelta(days=5),
            num_of_passengers=4,
            total_cost=100,
            rate=5
        )

    def test_invalid_token(self):
        response = client.get(
            reverse('villa:show_most_popular_city'),
            HTTP_AUTHORIZATION='Token {}'.format(self.invalid_token),
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_invalid_requestParams(self):
        response = client.get(
            reverse('villa:show_most_popular_city'),
            data={},
            HTTP_AUTHORIZATION='Token {}'.format(self.valid_token),
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_show_MostPopularCity(self):
        tests = [
            {'number_of_city': 0},
            {'number_of_city': 2},
            {'number_of_city': 1},
            {'country': 'USA', 'number_of_city': 2},
            {'country': 'Iran', 'state': 'Tehran', 'number_of_city': 2}
        ]
        outputs = [
            [],
            [
                {'country': 'Iran', 'state': 'Esfahan', 'city': 'Esfahan', 'no_villa': 2},
                {'country': 'Iran', 'state': 'Tehran', 'city': 'Tehran', 'no_villa': 1}
            ],
            [
                {'country': 'Iran', 'state': 'Esfahan', 'city': 'Esfahan', 'no_villa': 2}
            ],
            [],
            [
                {'country': 'Iran', 'state': 'Tehran', 'city': 'Tehran', 'no_villa': 1}
            ]
        ]

        for test in range(len(tests)):
            responce = client.get(
                reverse("villa:show_most_popular_city"),
                data=tests[test],
                HTTP_AUTHORIZATION='Token {}'.format(self.valid_token)
            )
            self.assertListEqual(responce.data['data'], outputs[test])


class MostRegisteredVillasTest(TestCase):
    def setUp(self) -> None:
        new_user = Account.objects.create(
            first_name='Danial',
            last_name='Bazmandeh',
            email='danibazi@gmail.com',
            phone_number='+989152147654',
            gender='Male',
            password='123456'
        )
        new_user.username = new_user.email
        new_user.save()

        self.valid_token, self.created = Token.objects.get_or_create(user=new_user)
        self.invalid_token = 'fasdfs45dsfasd1fsfasdf4dfassf13'

        owner = Account.objects.create(
            first_name='Danial',
            last_name='Bazmandeh',
            email='danibazi9@gmail.com',
            phone_number='+989152147655',
            gender='Male',
            password='123456'
        )
        owner.username = owner.email
        owner.save()

        customer = Account.objects.create(
            first_name='Sadegh',
            last_name='Jafari',
            email='sadeghjafari@gmail.com',
            phone_number='+989152147501',
            gender='Male',
            password='123456'
        )
        customer.username = customer.email
        customer.save()

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
            capacity=10,
            max_capacity=20,
            postal_code='1234'
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
            capacity=10,
            max_capacity=20,
            postal_code='1235'
        )

        Calendar.objects.create(
            customer=customer,
            villa=v1,
            start_date=datetime.now(),
            end_date=datetime.now() + timedelta(days=1),
            num_of_passengers=10,
            total_cost=50
        )

        Calendar.objects.create(
            customer=customer,
            villa=v1,
            start_date=datetime.now() + timedelta(days=3),
            end_date=datetime.now() + timedelta(days=5),
            num_of_passengers=5,
            total_cost=40
        )

        Calendar.objects.create(
            customer=customer,
            villa=v2,
            start_date=datetime.now() + timedelta(days=3),
            end_date=datetime.now() + timedelta(days=5),
            num_of_passengers=4,
            total_cost=100
        )

        Calendar.objects.create(
            customer=customer,
            villa=v2,
            start_date=datetime.now() + timedelta(days=3),
            end_date=datetime.now() + timedelta(days=5),
            num_of_passengers=5,
            total_cost=40
        )

        Calendar.objects.create(
            customer=customer,
            villa=v2,
            start_date=datetime.now() + timedelta(days=3),
            end_date=datetime.now() + timedelta(days=5),
            num_of_passengers=4,
            total_cost=100
        )

    def test_invalid_token(self):
        response = client.get(
            reverse('villa:show_most_registered_villas'),
            HTTP_AUTHORIZATION='Token {}'.format(self.invalid_token),
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_invalid_requestParams(self):
        response = client.get(
            reverse('villa:show_most_registered_villas'),
            data={},
            HTTP_AUTHORIZATION='Token {}'.format(self.valid_token),
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_show_MostRegisterVillas(self):
        tests = [{'number_of_villa': 2}, {'number_of_villa': 1}, {'number_of_villa': 0}]
        outputs = [[2, 1], [2], []]

        for test in range(len(tests)):
            responce = client.get(
                reverse("villa:show_most_registered_villas"),
                data=tests[test],
                HTTP_AUTHORIZATION='Token {}'.format(self.valid_token)
            )
            result = [v['villa_id'] for v in responce.data['data']]
            self.assertEquals(result, outputs[test])


class MostRatedVillasTest(TestCase):
    def setUp(self) -> None:
        new_user = Account.objects.create(
            first_name='Danial',
            last_name='Bazmandeh',
            email='danibazi@gmail.com',
            phone_number='+989152147654',
            gender='Male',
            password='123456'
        )
        new_user.username = new_user.email
        new_user.save()

        self.valid_token, self.created = Token.objects.get_or_create(user=new_user)
        self.invalid_token = 'fasdfs45dsfasd1fsfasdf4dfassf13'

        owner = Account.objects.create(
            first_name='Danial',
            last_name='Bazmandeh',
            email='danibazi9@gmail.com',
            phone_number='+989152147655',
            gender='Male',
            password='123456'
        )
        owner.username = owner.email
        owner.save()

        customer = Account.objects.create(
            first_name='Sadegh',
            last_name='Jafari',
            email='sadeghjafari@gmail.com',
            phone_number='+989152147501',
            gender='Male',
            password='123456'
        )
        customer.username = customer.email
        customer.save()

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
            capacity=10,
            max_capacity=20,
            postal_code='1234',
            rate=3,
            no_rate=1
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
            capacity=10,
            max_capacity=20,
            postal_code='1235',
            rate=4,
            no_rate=1
        )

    def test_invalid_token(self):
        response = client.get(
            reverse('villa:show_most_registered_villas'),
            HTTP_AUTHORIZATION='Token {}'.format(self.invalid_token),
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_invalid_requestParams(self):
        response = client.get(
            reverse('villa:show_most_registered_villas'),
            data={},
            HTTP_AUTHORIZATION='Token {}'.format(self.valid_token),
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_show_MostRatedVillas(self):
        tests = [{'number_of_villa': 2}, {'number_of_villa': 1}, {'number_of_villa': 0}]
        outputs = [[2, 1], [2], []]

        for test in range(len(tests)):
            responce = client.get(
                reverse("villa:show_most_rated_villas"),
                data=tests[test],
                HTTP_AUTHORIZATION='Token {}'.format(self.valid_token)
            )
            result = [v['villa_id'] for v in responce.data['data']]
            self.assertEquals(result, outputs[test])


class AddVillaRateTest(TestCase):
    def setUp(self) -> None:

        owner = Account.objects.create(
            first_name='Danial',
            last_name='Bazmandeh',
            email='danibazi9@gmail.com',
            phone_number='+989152147655',
            gender='Male',
            password='123456'
        )
        owner.username = owner.email
        owner.save()

        customer = Account.objects.create(
            first_name='Sadegh',
            last_name='Jafari',
            email='sadeghjafari@gmail.com',
            phone_number='+989152147501',
            gender='Male',
            password='123456'
        )
        customer.username = customer.email
        customer.save()

        self.valid_token, self.created = Token.objects.get_or_create(user=customer)
        self.invalid_token = 'fasdfs45dsfasd1fsfasdf4dfassf13'

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
            capacity=10,
            max_capacity=20,
            postal_code='1234',
            rate = 4,
            no_rate = 4
        )

        self.reserve = Calendar.objects.create(
            customer=customer,
            villa=v1,
            start_date=datetime.now(),
            end_date=datetime.now() + timedelta(days=1),
            num_of_passengers=10,
            total_cost=50,
        )


    def test_invalid_token(self):
        response = client.post(
            reverse('villa:add_rate'),
            HTTP_AUTHORIZATION='Token {}'.format(self.invalid_token),
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_invalid_requestParams(self):
        response = client.post(
            reverse('villa:add_rate'),
            data={},
            HTTP_AUTHORIZATION='Token {}'.format(self.valid_token),
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_does_not_exist_reserve(self):
        response = client.post(
            reverse('villa:add_rate'),
            data = {'villa_id':20, 'rate':5},
            HTTP_AUTHORIZATION='Token {}'.format(self.valid_token),
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_add_rate_currectly(self):
        response = client.post(
            reverse('villa:add_rate'),
            data = {'villa_id':self.reserve.villa.villa_id, 'rate':5},
            HTTP_AUTHORIZATION='Token {}'.format(self.valid_token),
        )
        self.assertEqual(response.data['data']['rate'], 4.2)


class LikeVillaTest(TestCase):
    """ Test module for like/dislike villa by user """

    def setUp(self):
        new_user = Account.objects.create(
            first_name='Danial',
            last_name='Bazmandeh',
            email='danibazi9@gmail.com',
            phone_number='+989152147655',
            gender='Male',
            password='123456'
        )

        villa = Villa.objects.create(
            name='My Villa',
            type='Coastal',
            price_per_night=2300,
            country='Iran',
            state='Mazandaran',
            city='Sari',
            address='St 2.',
            postal_code='9738920343',
            latitude=31.2458,
            longitude=35.25478,
            area=150,
            owner=new_user,
            capacity=10,
            max_capacity=15,
            number_of_bathrooms=2,
            number_of_bedrooms=2,
            number_of_single_beds=1,
            number_of_double_beds=1,
            number_of_showers=1
        )

        self.valid_token, self.created = Token.objects.get_or_create(user=new_user)
        self.invalid_token = 'fasdfs45dsfasd1fsfasdf4dfassf13'
        self.villa_id = villa.villa_id

        self.valid_like = {
            'villa_id': villa.villa_id,
            'like': 'true'
        }

        self.valid_dislike = {
            'villa_id': villa.villa_id,
            'like': 'false'
        }

        self.invalid_like = {
            'villa_id': villa.villa_id,
        }

        self.invalid_like2 = {
            'villa_id': villa.villa_id,
            'like': 'xx'
        }

        self.invalid_like3 = {
            'like': 'true'
        }

        self.invalid_like4 = {
            'villa_id': 4,
            'like': 'true'
        }

    def test_valid_like_villa(self):
        response = client.post(
            reverse('villa:like_villa'),
            data=self.valid_like,
            HTTP_AUTHORIZATION='Token {}'.format(self.valid_token),
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        my_villa = Villa.objects.get(villa_id=self.villa_id)
        self.assertEqual(my_villa.likes.count(), 1)

    def test_valid_dislike_villa(self):
        response = client.post(
            reverse('villa:like_villa'),
            data=self.valid_dislike,
            HTTP_AUTHORIZATION='Token {}'.format(self.valid_token),
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        my_villa = Villa.objects.get(villa_id=self.villa_id)
        self.assertEqual(my_villa.likes.count(), 0)

    def test_invalid_like_villa(self):
        response = client.post(
            reverse('villa:like_villa'),
            data=self.invalid_like,
            HTTP_AUTHORIZATION='Token {}'.format(self.valid_token),
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = client.post(
            reverse('villa:like_villa'),
            data=self.invalid_like,
            HTTP_AUTHORIZATION='Token {}'.format(self.valid_token),
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = client.post(
            reverse('villa:like_villa'),
            data=self.invalid_like2,
            HTTP_AUTHORIZATION='Token {}'.format(self.valid_token),
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = client.post(
            reverse('villa:like_villa'),
            data=self.invalid_like3,
            HTTP_AUTHORIZATION='Token {}'.format(self.valid_token),
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = client.post(
            reverse('villa:like_villa'),
            data=self.invalid_like4,
            HTTP_AUTHORIZATION='Token {}'.format(self.valid_token),
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_like_villa_unauthorized(self):
        response = client.post(
            reverse('villa:like_villa'),
            data=self.valid_like,
            HTTP_AUTHORIZATION='Token {}'.format(self.invalid_token),
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class CheckGetFavoriteVillas(TestCase):
    """ Test module for get favorite villas of each user """

    def setUp(self):
        self.new_user = Account.objects.create(
            first_name='Danial',
            last_name='Bazmandeh',
            email='danibazi9@gmail.com',
            phone_number='+989152147655',
            gender='Male',
            password='123456'
        )

        new_villa = Villa.objects.create(
            name='My Villa',
            type='Coastal',
            price_per_night=3456765432234567,
            country='Iran',
            state='Mazandaran',
            city='Sari',
            address='St 2.',
            postal_code='9738920343',
            latitude=0,
            longitude=0,
            area=15200,
            owner=self.new_user,
            capacity=10,
            max_capacity=15,
            number_of_bathrooms=234564324,
            number_of_bedrooms=2344534,
            number_of_single_beds=2343454,
            number_of_double_beds=14444,
            number_of_showers=4452
        )

        new_villa.likes.add(self.new_user)

        self.valid_token, self.created = Token.objects.get_or_create(user=self.new_user)

        self.invalid_token = 'fasdfs45dsfasd1fsfasdf4dfassf13'

    def test_get_favorite_villas_authorized(self):
        response = client.get(
            reverse('villa:get_favorite_villas'),
            HTTP_AUTHORIZATION='Token {}'.format(self.valid_token.key),
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['data']), len(Villa.objects.filter(likes__user_id=self.new_user.user_id)))

        for villa in response.data['data']:
            self.assertEqual(villa['name'], 'My Villa')
            self.assertEqual(villa['country'], 'Iran')
            self.assertEqual(villa['state'], 'Mazandaran')
            self.assertEqual(villa['city'], 'Sari')
            self.assertEqual(villa['owner'], self.new_user.__str__())

    def test_get_favorite_villas_unauthorized(self):
        response = client.get(
            reverse('villa:get_favorite_villas'),
            HTTP_AUTHORIZATION='Token {}'.format(self.invalid_token),
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class CheckPostalCode(TestCase):
    """ Test module for checking postal code of villa (must unique) """

    def setUp(self):
        new_user = Account.objects.create(
            first_name='Danial',
            last_name='Bazmandeh',
            email='danibazi9@gmail.com',
            phone_number='+989152147655',
            gender='Male',
            password='123456'
        )

        Villa.objects.create(
            name='My Villa',
            type='Coastal',
            price_per_night=3456765432234567,
            country='Iran',
            state='Mazandaran',
            city='Sari',
            address='St 2.',
            postal_code='9738920343',
            latitude=0,
            longitude=0,
            area=15200,
            owner=new_user,
            capacity=10,
            max_capacity=15,
            number_of_bathrooms=234564324,
            number_of_bedrooms=2344534,
            number_of_single_beds=2343454,
            number_of_double_beds=14444,
            number_of_showers=4452
        )

        self.invalid_data = {
        }

        self.invalid_data2 = {
            'p': '9738920343'
        }

        self.unique_data = {
            'postal_code': '1230245687'
        }

        self.redundant_data = {
            'postal_code': '9738920343'
        }

        self.valid_token, self.created = Token.objects.get_or_create(user=new_user)

        self.invalid_token = 'fasdfs45dsfasd1fsfasdf4dfassf13'

    def test_unique_check_postal_code(self):
        response = client.post(
            reverse('villa:check_postal_code'),
            data=self.unique_data,
            HTTP_AUTHORIZATION='Token {}'.format(self.valid_token),
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_redundant_check_postal_code(self):
        response = client.post(
            reverse('villa:check_postal_code'),
            data=self.redundant_data,
            HTTP_AUTHORIZATION='Token {}'.format(self.valid_token),
        )
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)

    def test_invalid_check_postal_code(self):
        response = client.post(
            reverse('villa:check_postal_code'),
            data=self.invalid_data,
            HTTP_AUTHORIZATION='Token {}'.format(self.valid_token),
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = client.post(
            reverse('villa:check_postal_code'),
            data=self.invalid_data2,
            HTTP_AUTHORIZATION='Token {}'.format(self.valid_token),
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_check_postal_code_unauthorized(self):
        response = client.post(
            reverse('villa:check_postal_code'),
            data=self.unique_data,
            HTTP_AUTHORIZATION='Token {}'.format(self.invalid_token),
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
