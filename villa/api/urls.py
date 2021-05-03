from django.urls import path
from villa.api import views

app_name = 'villa'

urlpatterns = [
    path('user/all/', views.get_all_villas, name='get_all_villas'),
    path('user/', views.UserVilla.as_view(), name='villa_apis'),
    path('user/images/', views.upload_image, name='upload_image'),
    path('user/documents/', views.upload_document, name='upload_document'),
    path('search/', views.search, name='search'),
    path('calendar/show/', views.show_villa_calendar,name='show_calendar')
]
