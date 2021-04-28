from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.db import models

def upload_to(instance, filename):
    return 'forum/{filename}'.format(filename=filename)

class Publicacion(models.Model):
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    tema = models.CharField(max_length=40)
    titulo = models.CharField(max_length=60)
    contenido = models.TextField()
    fecha = models.DateTimeField(default=timezone.now)
    imagen1 = models.ImageField(_("Image1"), upload_to=upload_to, default='forum/image1.png')
    imagen2 = models.ImageField(_("Image2"), upload_to=upload_to, default='forum/image1.png')
    imagen3 = models.ImageField(_("Image3"), upload_to=upload_to, default='forum/image1.png')

    def __str__(self):
        return self.autor.username + " --- " + self.titulo
    