from django.urls import path
from . import views

app_name = 'sync'

urlpatterns = [
    path('control/', views.control, name='control'),
    path('control/usuario/<str:id>/', views.control_usuario, name='control_usuario'),
    path('control/usuario/crear_eliminar_usuario/<str:id>/', views.crear_eliminar_usuario, name='crear_eliminar_usuario'),
    path('control/perfil/<str:id>/', views.control_perfil, name='control_perfil'),
    path('control/usuario/actualizar_perfil/<str:id>/', views.actualizar_perfil, name='actualizar_perfil'),
    path('control/servicio/<str:id>/', views.control_servicio, name='control_servicio'),
]
