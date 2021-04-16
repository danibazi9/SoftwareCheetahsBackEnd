from django.test import TestCase

from account.models import Account


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
