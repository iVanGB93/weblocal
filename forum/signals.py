from django.db.models.signals import post_save
from django.dispatch import receiver
from forum.models import Publicacion

from sync.actions import UpdateThreadForum

@receiver(post_save, sender=Publicacion)
def actualizar_publicacion(sender, instance, **kwargs):
    if not instance.sync:
        data = {'id': instance.id, 'usuario': instance.autor.username, 'tema': instance.tema, 'titulo': instance.titulo, 'contenido': instance.contenido}
        UpdateThreadForum(data).start()