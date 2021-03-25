from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Profile
from django.contrib.auth.models import  User


@receiver(post_save, sender=User)
def crearProfile(sender, instance, **kwargs):
    usuario = instance.username
    usuario = User.objects.get(username=usuario)
    if Profile.objects.filter(usuario=usuario).exists():
        pass
    else:        
        profile = Profile(usuario=usuario)
        profile.save()