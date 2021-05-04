import json

from django.test import TestCase, Client

from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token

from account.models import Account

# initialize the APIClient app
client = Client()
 
