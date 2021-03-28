from django.urls import path

from account.api.views import *

app_name = 'account'

urlpatterns = [
    path('register', registration_view, name='register'),
    path('properties/update', update_account_view, name='update'),
    path('login', TokenObtainView.as_view(), name='login'),
    path('logout', logoutView.as_view(), name='logout'),
    path('properties', account_properties_view, name="properties"),
    path('send-email', SendEmail.as_view()),
    path('properties/all', all_acounts_view, name="properties_all"),
]
