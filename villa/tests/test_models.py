from unittest import mock

from django.core.files import File
from django.test import TestCase

from villa.models import *


class VillaTest(TestCase):
    """ Test module for Villa model """

    def setUp(self):
        new_user = Account.objects.create(
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
            price_per_night=2500,
            country='Iran',
            state='Mazandaran',
            city='Sari',
            address='St 2.',
            postal_code='9738920480',
            latitude=0,
            longitude=0,
            area=15200,
            owner=new_user,
            capacity=10,
            max_capacity=15,
            number_of_bathrooms=2,
            number_of_bedrooms=3,
            number_of_single_beds=2,
            number_of_double_beds=1,
            number_of_showers=2
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

    def test_villa_str(self):
        villa = Villa.objects.get(name='My Villa')
        self.assertEqual(villa.__str__(), 'My Villa, Owner: Danial Bazmandeh')

        villa = Villa.objects.get(country='Irannnnsdfthg3$%#@#')
        self.assertEqual(villa.__str__(), 'My Villaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa3453342@$%@$%^^56'
                                          '#7865xcvxcvxv2345665DFSDFDSasdasd4, Owner: Danial Bazmandeh')

    def test_villa_type(self):
        villa = Villa.objects.get(name='My Villa')
        self.assertEqual(villa.postal_code, '9738920480')

        villa = Villa.objects.get(country='Irannnnsdfthg3$%#@#')
        self.assertEqual(villa.postal_code, '9738920343')

    def test_villa_price_per_night(self):
        villa = Villa.objects.get(name='My Villa')
        self.assertEqual(villa.price_per_night, 2500)

        villa = Villa.objects.get(country='Irannnnsdfthg3$%#@#')
        self.assertEqual(villa.price_per_night, 3456765432234567)

    def test_villa_capacity(self):
        villa = Villa.objects.get(name='My Villa')
        self.assertEqual(villa.capacity, 10)

        villa = Villa.objects.get(country='Irannnnsdfthg3$%#@#')
        self.assertEqual(villa.capacity, 10)

    def test_villa_documents(self):
        villa = Villa.objects.get(name='My Villa')

        file_mock = mock.MagicMock(spec=File)
        file_mock.name = 'test.pdf'

        new_document1 = Document.objects.create(
            file=file_mock
        )

        villa.documents.add(new_document1)

        self.assertEqual(villa.documents.get(document_id=new_document1.document_id), new_document1)

    def test_villa_facilities(self):
        villa = Villa.objects.get(name='My Villa')

        new_facility = Facility.objects.create(name='Washer')
        villa.facilities.add(new_facility)

        self.assertEqual(villa.facilities.get(facility_id=new_facility.facility_id), new_facility)

        new_facility = Facility.objects.create(name='sdfrsrdfyghkikhgfdr34354u6tjf32456u67t67yfyh')
        villa.facilities.add(new_facility)

        self.assertEqual(villa.facilities.get(facility_id=new_facility.facility_id), new_facility)

    def test_villa_images(self):
        villa = Villa.objects.get(name='My Villa')

        file_mock = mock.MagicMock(spec=File)
        file_mock.name = 'test.jpg'

        new_image = Image.objects.create(
            image=file_mock
        )

        villa.images.add(new_image)

        self.assertEqual(villa.images.get(image_id=new_image.image_id), new_image)

        file_mock = mock.MagicMock(spec=File)
        file_mock.name = 'aERWE6YUJNBV232435JRYWQ345U6RYJGB.jpg'

        new_image = Image.objects.create(
            image=file_mock
        )

        villa.images.add(new_image)

        self.assertEqual(villa.images.get(image_id=new_image.image_id), new_image)
