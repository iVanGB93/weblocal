from django.contrib.auth.models import User
from django.utils import timezone
from django.db import models

class Sorteo(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=10, unique=True)
    servicio = models.CharField(max_length=15)
    eliminado = models.BooleanField(default=False)
    fecha = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.usuario.username +  " " + self.servicio
    