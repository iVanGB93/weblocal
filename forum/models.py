from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.db import models

def upload_to(instance, filename):
    return 'forum/{filename}'.format(filename=filename)

class Publicacion(models.Model):
    opcionesTema = (
        ('Noticia', 'Noticia'),
        ('Internet', 'Internet'),
        ('JovenClub', 'JovenClub'),
        ('Emby', 'Emby'),
        ('FileZilla', 'FileZilla'),
        ('QbaRed', 'QbaRed'),
    )
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    tema = models.CharField(max_length=15, choices=opcionesTema)
    titulo = models.CharField(max_length=60)
    contenido = models.TextField()
    fecha = models.DateTimeField(default=timezone.now)
    online= models.BooleanField(default=False)
    visitas = models.PositiveIntegerField(default=0)
    imagen1 = models.ImageField(_("Imagen1"), upload_to=upload_to, default='forum/image1.png')
    imagen2 = models.ImageField(_("Imagen2"), upload_to=upload_to, default='forum/image1.png')
    imagen3 = models.ImageField(_("Imagen3"), upload_to=upload_to, default='forum/image1.png')

    def __str__(self):
        return "Usuario: " + self.autor.username + " tema: " + self.tema +  " título: " + self.titulo
    