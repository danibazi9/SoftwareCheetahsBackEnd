from django.urls import path

from account.api.views import *

app_name = 'account'

urlpatterns = [
    path('register', registration_view, name='register'),
    path('properties/update', update_account_view, name='update'),
    path('login', TokenObtainView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('properties', account_properties_view, name="properties"),
    path('send-email', send_email, name='send_email'),
    path('properties/all', all_accounts_view, name="properties_all"),
    path('check-existence', check_email_existence, name="check-existence"),
    path('upload-documents', upload_document),
    path('check-document-existence', check_document_existence),
    path('update_account_image', update_account_image, name="update_account_image"),
    path('show_account_image', show_account_image, name="show_account_image"),
]
