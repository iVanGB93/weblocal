from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

""" def pk_mensaje():
    while True:
        pk = 1
        if Mensaje.objects.filter(pk=pk).exists():
            pk = pk + 1
        else:
            break
    return pk

def pk_chat():
    while True:
        pk = 1
        if Chat.objects.filter(pk=pk).exists():
            pk = pk + 1
        else:
            break
    return pk """

class Mensaje(models.Model):
    #id = models.IntegerField(primary_key=True, unique=True, default=pk_mensaje)
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    contenido = models.TextField()
    fecha = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return "Mensaje: " + self.contenido + ", de: " + self.autor.username

class Chat(models.Model):
    #id = models.IntegerField(primary_key=True, unique=True, default=pk_chat)
    participantes = models.ManyToManyField(User)
    mensajes = models.ManyToManyField(Mensaje)
    grupo = models.BooleanField(default=False)
    fecha = models.DateTimeField(default=timezone.now)