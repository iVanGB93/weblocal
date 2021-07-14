from apscheduler.schedulers.background import BackgroundScheduler
from decouple import config
import os

from .models import EstadoConexion

def chequeo_conexion_online():
    print("CHEQUEANDO SI ESTA ONLINE EL SERVER")
    servidor = config('NOMBRE_SERVIDOR')
    ip_online = config('IP_ONLINE')
    if EstadoConexion.objects.filter(id=1).exists():
        conexion = EstadoConexion.objects.get(id=1)
    else:
        conexion = EstadoConexion(id=1, servidor=servidor, ip_online=ip_online)
    response = os.popen(f"ping { ip_online }").read()
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
    scheduler.add_job(chequeo_conexion_online, 'interval', minutes=4)
    scheduler.add_job(chequeo_conexion_servicios, 'interval', minutes=40)
    scheduler.start()
