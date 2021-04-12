from django.urls import path
from villa.api import views

app_name = 'villa'

urlpatterns = [
    path('user/all/', views.get_all_villas),
    path('user/', views.Villa.as_view()),
]
