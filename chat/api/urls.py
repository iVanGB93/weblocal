from .views import ContactView
from django.urls import path

app_name='chat-api'


urlpatterns = [
    path('contactos/<str:pk>/', ContactView.as_view(), name='contactos'),
]