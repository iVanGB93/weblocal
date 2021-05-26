from django.db.models.signals import post_save
from django.dispatch import receiver
from servicios.models import Oper, EstadoServicio
from django.contrib.auth.models import  User
from sync.syncs import actualizacion_remota
from django.core.mail import send_mail

@receiver(post_save, sender=User)
def crearServicios(sender, instance, **kwargs):
    usuario = instance.username
    usuario = User.objects.get(username=usuario)
    if EstadoServicio.objects.filter(usuario=usuario).exists():
        pass
    else:        
        servicios = EstadoServicio(usuario=usuario)
        servicios.save()

@receiver(post_save, sender=Oper)
def correoOper(sender, instance, **kwargs):
    usuario = instance.usuario
    servicio = instance.servicio
    cantidad = instance.cantidad
    fecha = instance.fecha
    data = {'code': instance.code, 'tipo': instance.tipo, 'usuario': instance.usuario, 'servicio': instance.servicio, 'cantidad': instance.cantidad, 'codRec': instance.codRec, 'haciaDesde': instance.haciaDesde, 'fecha': instance.fecha}
    respuesta = actualizacion_remota('nueva_operacion', data)
    if not respuesta['estado']:
        send_mail(f'Falló al subir el servicio', f'La operación de { instance.tipo } del usuario {usuario} no se pudo sincronizar con internet. Fecha: { fecha}.', 'RedCentroHabanaCuba@gmail.com', ['ivanguachbeltran@gmail.com'])    
    if instance.tipo == 'PAGO':
        send_mail(f'Pago Realizado -- { usuario }', f'El usuario { usuario } pagó { cantidad } por { servicio }. Fecha: { fecha}', 'RedCentroHabanaCuba@gmail.com', ['ivanguachbeltran@gmail.com'])
    elif instance.tipo == 'RECARGA':
        send_mail(f'{ usuario } ha recargado', f'El usuario { usuario } agregó { cantidad } a su cuenta. Código: { instance.codRec }. Fecha: { fecha}', 'RedCentroHabanaCuba@gmail.com', ['ivanguachbeltran@gmail.com'])
    elif instance.tipo == 'ENVIO':
        send_mail(f'{ usuario } realizó un envio', f'El usuario { usuario } envió { cantidad } a { instance.haciaDesde }. Fecha: { fecha}', 'RedCentroHabanaCuba@gmail.com', ['ivanguachbeltran@gmail.com'])
    elif instance == 'RECIBO':
        send_mail(f'{ usuario } ha recibido', f'El usuario { usuario } recibió { cantidad } de { instance.haciaDesde }. Fecha: { fecha}', 'RedCentroHabanaCuba@gmail.com', ['ivanguachbeltran@gmail.com'])
