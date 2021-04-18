from django.urls import path
from villa.api import views

app_name = 'villa'

urlpatterns = [
    path('user/all/', views.get_all_villas),
    path('user/', views.UserVilla.as_view()),
    path('user/images/', views.upload_image),
    path('user/documents/', views.upload_document),
    path('user/check-document-existence/', views.check_document_existence),
    path('search/',views.search,name='search')
]
