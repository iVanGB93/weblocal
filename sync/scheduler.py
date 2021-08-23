from apscheduler.schedulers.background import BackgroundScheduler
from decouple import config
import os

from django.utils import timezone
from .syncs import actualizacion_remota
from .models import EstadoConexion

def chequeo_conexion_online():
    print("CHEQUEANDO SI ESTA ONLINE EL SERVER")
    servidor = config('NOMBRE_SERVIDOR')
    ip_online = config('IP_ONLINE')
    if EstadoConexion.objects.filter(id=1).exists():
        conexion = EstadoConexion.objects.get(id=1)
    else:
        conexion = EstadoConexion(id=1, servidor=servidor, ip_online=ip_online)
        conexion.ip_internet = config('IP_INTERNET')
        conexion.ip_jc = config('IP_JC')
        conexion.ip_emby = config('IP_EMBY')
        conexion.ip_ftp = config('IP_FTP')
    data = {'identidad': servidor}
    respuesta = actualizacion_remota('saludo', data)
    if respuesta['estado']:
        print("SERVIDOR ONLINE")
        conexion.online = True
    else:
        print("NO TIENE INTERNET EL SERVIDOR", respuesta['mensaje'])
        conexion.online = False
    conexion.save()


def chequeo_conexion_servicios():
    print("CHEQUEANDO LOS SERVICIOS")    
    conexion = EstadoConexion.objects.get(id=1)
    response = os.popen(f"ping { conexion.ip_internet }").read()
    if "recibidos = 4" in response:
        print("INTERNET ONLINE")
        conexion.internet = True
    else:
        print("INTERNET CAIDO")
        conexion.internet = False
    response = os.popen(f"ping { conexion.ip_jc }").read()
    if "recibidos = 4" in response:
        print("JC ONLINE")
        conexion.jc = True
    else:
        print("JC CAIDO")
        conexion.jc = False
    response = os.popen(f"ping { conexion.ip_emby }").read()
    if "recibidos = 4" in response:
        print("EMBY ONLINE")
        conexion.emby = True
    else:
        print("EMBY CAIDO")
        conexion.emby = False
    response = os.popen(f"ping { conexion.ip_ftp }").read()
    if "recibidos = 4" in response:
        print("FTP ONLINE")
        conexion.ftp = True
    else:
        print("FTP CAIDO")
        conexion.ftp = False
    conexion.fecha_internet = timezone.now()
    conexion.save()

#chequeo_conexion_online()


def chequeo_conexiones():
    scheduler = BackgroundScheduler()
    scheduler.add_job(chequeo_conexion_online, 'interval', minutes=3)
    scheduler.add_job(chequeo_conexion_servicios, 'interval', minutes=40)
    scheduler.start()
