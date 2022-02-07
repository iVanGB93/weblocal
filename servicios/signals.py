from django.db.models.signals import post_save
from django.dispatch import receiver
from servicios.models import Oper, EstadoServicio, Recarga
from django.contrib.auth.models import  User
from servicios.api.serializers import ServiciosSerializer
from django.core.mail import EmailMessage
from decouple import config

from sync.actions import EmailSending, UpdateThreadServicio, UpdateThreadOper, UpdateThreadRecarga

@receiver(post_save, sender=User)
def crearServicios(sender, instance, **kwargs):
    usuario = instance.username
    usuario = User.objects.get(username=usuario)
    if EstadoServicio.objects.filter(usuario=usuario).exists():
        pass
    else:        
        servicios = EstadoServicio(usuario=usuario)
        servicios.sync = True
        servicios.save()

@receiver(post_save, sender=Oper)
def correoOper(sender, instance, **kwargs):
    usuario = str(instance.usuario)
    if instance.servicio != None:
        servicio = instance.servicio
    else:
        servicio = 'None'
    if instance.codRec != None:
        codRec = instance.codRec
    else:
        codRec = 'None'
    if instance.haciaDesde != None:
        haciaDesde = str(instance.haciaDesde)
    else:
        haciaDesde = 'None'
    cantidad = instance.cantidad
    fecha = str(instance.fecha)
    online = config('APP_MODE')
    if online == 'online':
        if instance.sync == False:
            data = {'code': instance.code, 'tipo': instance.tipo, 'usuario': usuario, 'servicio': servicio, 'cantidad': instance.cantidad, 'codRec': codRec, 'haciaDesde': haciaDesde, 'fecha': fecha}
            UpdateThreadOper(data).start()                    
            if instance.tipo == 'PAGO':
                email = EmailMessage(f'Pago Realizado -- { usuario }', f'El usuario { usuario } pagó { cantidad } por { servicio }. Fecha: { fecha}', None, ['ivanguachbeltran@gmail.com', 'javymk9026@gmail.com'])
                EmailSending(email).start()
            elif instance.tipo == 'RECARGA':
                email = EmailMessage(f'{ usuario } ha recargado', f'El usuario { usuario } agregó { cantidad } a su cuenta. Código: { instance.codRec }. Fecha: { fecha}', None, ['ivanguachbeltran@gmail.com', 'javymk9026@gmail.com'])
                EmailSending(email).start()
            elif instance.tipo == 'ENVIO':
                email = EmailMessage(f'{ usuario } realizó un envio', f'El usuario { usuario } envió { cantidad } a { instance.haciaDesde }. Fecha: { fecha}', None, ['ivanguachbeltran@gmail.com', 'javymk9026@gmail.com'])
                EmailSending(email).start()
            elif instance == 'RECIBO':
                email = EmailMessage(f'{ usuario } ha recibido', f'El usuario { usuario } recibió { cantidad } de { instance.haciaDesde }. Fecha: { fecha}', None, ['ivanguachbeltran@gmail.com', 'javymk9026@gmail.com'])
                EmailSending(email).start()            

@receiver(post_save, sender=EstadoServicio)
def actualizar_servicios(sender, instance, **kwargs):
    online = config('APP_MODE')
    if online == 'online':
        if instance.sync == False:
            serializer = ServiciosSerializer(instance)
            data=serializer.data
            data['usuario'] = instance.usuario.username
            UpdateThreadServicio(data).start()            

@receiver(post_save, sender=Recarga)
def actualizar_recarga(sender, instance, **kwargs):
    if config('APP_MODE') == 'online':
        if instance.sync == False:
            data = {'code': instance.code, 'cantidad': instance.cantidad, 'fechaHecha': str(instance.fechaHecha)}
            UpdateThreadRecarga(data).start()