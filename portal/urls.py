from django.urls import path
from .views import index

app_name = 'portal'

urlpatterns = [    
    path('register/', index, name='index'),
    path('login/', index, name='index'),
    path('logout/', index, name='index'),
    path('servicios/internet/', index, name='index'),
    path('servicios/joven-club/', index, name='index'),
    path('servicios/emby/', index, name='index'),
    path('servicios/ftp/', index, name='index'),    
    path('perfil/datos/', index, name='index'),    
    path('coins/recarga/', index, name='index'),
    path('coins/transferir/', index, name='index'),
    path('coins/ultimasop/', index, name='index'),
    path('', index, name='index'),
]
