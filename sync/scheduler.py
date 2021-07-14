from apscheduler.schedulers.background import BackgroundScheduler
from decouple import config
import os

from .models import EstadoConexion

def chequeo_conexion_online():
    print("CHEQUEANDO SI ESTA ONLINE EL SERVER")
    servidor = config('NOMBRE_SERVIDOR')
    ip_online = config('IP_ONLINE')
    if EstadoConexion.objects.filter(servidor=servidor).exists():
        conexion = EstadoConexion.objects.get(servidor=servidor)
        conexion.ip_online = ip_online
    else:
        conexion = EstadoConexion(servidor=servidor)
        conexion.ip_online = ip_online
    ip = conexion.ip_online
    response = os.popen(f"ping { ip }").read()
    if "recibidos = 4" in response:
        print("SERVIDOR ONLINE")
        conexion.online = True
    else:
        print("NO TIENE INTERNET EL SERVIDOR")
        conexion.online = False
    conexion.save()


def chequeo_conexion_servicios():
    print("CHEQUEANDO LOS SERVICIOS")


chequeo_conexion_online()


def chequeo_conexiones():
    scheduler = BackgroundScheduler()
    scheduler.add_job(chequeo_conexion_online, 'interval', minutes=3)
    scheduler.add_job(chequeo_conexion_servicios, 'interval', minutes=30)
    scheduler.start()
