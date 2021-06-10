from django.urls import path

from . import views

urlpatterns = [
    path('add/', views.add_chat, name='add_chat'),
    path('show/', views.show_chat, name='show_chat')
]
