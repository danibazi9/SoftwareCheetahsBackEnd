from django.urls import path

from . import views

urlpatterns = [
    path('show-message/', views.show_message, name='show_message'),
]
