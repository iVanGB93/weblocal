from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path, re_path

from sorteo.consumers import WSConsumer
from sync.consumers import SyncWSConsumer

application = ProtocolTypeRouter({   
    "websocket": AuthMiddlewareStack(
        URLRouter([          
            path('ws/sync/', SyncWSConsumer.as_asgi()),
            re_path(r'ws/sorteo/(?P<room_name>\w+)/$', WSConsumer.as_asgi()),
        ]),
    ),
})




