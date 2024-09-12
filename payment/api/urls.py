from django.urls import path

from payment.api.views import *

app_name = 'payment'

urlpatterns = [
    path('charge/', charge, name='charge'),
    path('pay/', pay, name='pay'),

]
