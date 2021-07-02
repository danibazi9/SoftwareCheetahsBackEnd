from django.urls import path

from . import views

app_name = 'chat'

urlpatterns = [
    path('add/', views.add_chat, name='add_chat'),
    path('show/', views.show_chat, name='show_chat'),
    path('upload/', views.upload_file, name='upload_file')
]
