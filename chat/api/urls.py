from django.urls import path

from . import views

urlpatterns = [
    path('chat/add/', views.add_chat, name='add_chat'),
]
