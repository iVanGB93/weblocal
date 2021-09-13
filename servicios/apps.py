from django.apps import AppConfig
from django.conf import settings

class ServiciosConfig(AppConfig):
    name = 'servicios'

    def ready(self): 
        import servicios.signals
        if not settings.DEBUG:
            from .scheduler import tiempoAcabado       
            tiempoAcabado()
