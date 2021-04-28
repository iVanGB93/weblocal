from django.urls import path
from .views import index, detalles

app_name = 'forum'

urlpatterns = [
    path('', index, name='index'),
    path('<int:pk>/', detalles, name='detalles'),
]