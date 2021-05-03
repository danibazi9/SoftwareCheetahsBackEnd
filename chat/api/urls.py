from django.urls import path

from . import views

urlpatterns = [
    path('show_Message/', views.show_Message, name='show_Message'),
]
