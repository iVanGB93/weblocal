from django.urls import path
from . import views

app_name = 'sync'

urlpatterns = [
    path('nuevo_usuario', views.nuevo_usuario, name='nuevo_usuario'),
]
