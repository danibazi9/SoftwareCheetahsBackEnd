from django.urls import path
from villa.api import views

app_name = 'villa'

urlpatterns = [
    path('user/all/', views.get_all_villas),
    path('user/', views.UserVilla.as_view()),
    path('user/images/', views.upload_image),
    path('admin/remove-waste-images/', views.remove_waste_images),
]
