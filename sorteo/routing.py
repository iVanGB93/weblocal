from django.urls import path, re_path

from .consumers import WSConsumer

websocket_urlpatterns = [
    #path('ws/sorteo/running/', WSConsumer.as_asgi()),
    re_path(r'ws/sorteo/(?P<room_name>\w+)/$', WSConsumer.as_asgi()),
]
