from unittest import mock

from django.core.files import File
from django.test import TestCase

from account.models import Account, Document


class AccountTest(TestCase):
    """ Test module for Account model """

    def setUp(self):
        Account.objects.create(
            first_name='Danial',
            last_name='Bazmandeh',
            email='danibazi9@gmail.com',
            phone_number='+989152147655',
            gender='Male',
            password='123456'
        )

    def test_account_str(self):
        account = Account.objects.get(email='danibazi9@gmail.com')
        self.assertEqual(account.__str__(), 'Danial Bazmandeh')

    def test_account_phone_number(self):
        account = Account.objects.get(email='danibazi9@gmail.com')
        self.assertEqual(account.phone_number, '+989152147655')

    def test_account_gender(self):
        account = Account.objects.get(email='danibazi9@gmail.com')
        self.assertEqual(account.gender, 'Male')

    def test_account_documents(self):
        account = Account.objects.get(email='danibazi9@gmail.com')

        file_mock = mock.MagicMock(spec=File)
        file_mock.name = 'test.pdf'

        new_document = Document.objects.create(
            user=account,
            file=file_mock
        )

        self.assertEqual(Document.objects.get(user=account), new_document)
