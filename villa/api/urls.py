from django.urls import path
from villa.api import views

app_name = 'villa'

urlpatterns = [
    path('user/all/', views.get_all_villas, name='get_all_villas'),
    path('user/', views.UserVilla.as_view(), name='villa_apis'),
    path('user/images/', views.upload_image, name='upload_image'),
    path('user/documents/', views.upload_document, name='upload_document'),
    path('fixed-rules/', views.get_fixed_rules, name='get_fixed_rules'),
    path('special-rules/', views.get_special_rules, name='get_special_rules'),
]
