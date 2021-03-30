from django.urls import path

from account.api.views import *

app_name = 'account'

urlpatterns = [
    path('register', registration_view, name='register'),
    path('properties/update', update_account_view, name='update'),
    path('login', TokenObtainView.as_view(), name='login'),
    path('logout', logoutView.as_view(), name='logout'),
    path('properties', account_properties_view, name="properties"),
    path('send-email', send_email, name='send_email'),
    path('properties/all', all_accounts_view, name="properties_all"),
    path('checkUniqueness/', checkUniqueness, name="checkUniqueness"),
]
