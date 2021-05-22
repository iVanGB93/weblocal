from django.urls import path
from . import views

app_name = 'sync'

urlpatterns = [
    path('control/', views.control, name='control'),
    path('control/usuario/<str:id>/', views.control_usuario, name='control_usuario'),
    path('control/usuario/crear_eliminar/<str:id>/', views.crear_eliminar, name='crear_eliminar'),
    path('control/servicio/<str:id>/', views.control_servicio, name='control_servicio'),
]
