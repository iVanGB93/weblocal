from django.urls import path
from .views import index, running

app_name = 'sorteo'

urlpatterns = [
    path('', index, name='index'),
    path('running/', running, name='running'),
]