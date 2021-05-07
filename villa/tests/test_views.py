import os

from django.test import TestCase, Client

from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token

from villa.models import *

# initialize the APIClient app
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
