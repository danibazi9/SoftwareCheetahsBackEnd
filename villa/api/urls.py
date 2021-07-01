from django.urls import path
from villa.api import views

app_name = 'villa'

urlpatterns = [
    path('user/all/', views.get_all_villas, name='get_all_villas'),
    path('user/', views.UserVilla.as_view(), name='villa_apis'),
    path('user/likes/', views.get_favourite_villas, name='favourite_villas'),
    path('user/images/', views.upload_image, name='upload_image'),
    path('user/documents/', views.upload_document, name='upload_document'),
    path('fixed-rules/', views.get_fixed_rules, name='get_fixed_rules'),
    path('special-rules/', views.get_special_rules, name='get_special_rules'),
    path('user/register/', views.register_villa, name='register_villa'),
    path('search/',views.search,name='search'),
    path('calendar/show/', views.show_villa_calendar, name='show_calendar'),
    path('most-popular-city/show/', views.get_most_reserved_city, name='show_most_popular_city'),
    path('most-registered/show/', views.show_most_registered_villas, name='show_most_registered_villas'),
    path('most-rated/show/', views.show_most_rated_villas, name='show_most_rated_villas'),
    path('rate/add/', views.add_rate, name='add_rate'),
    path('like/', views.like_villa, name='like_villa')
]
