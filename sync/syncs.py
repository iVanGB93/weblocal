#from django.contrib.auth.models import User
from decouple import config
import asyncio
import websockets
import json

medula = config('MEDULA')

def actualizacion_usuario(method, usuario, email=None, password=None, data=None):
    if method == 'check':
        print("CHECKING")
        data = {'usuario': usuario}
        recibe = asyncio.get_event_loop().run_until_complete(conectar(medula, 'check_usuario', data))
        print(recibe, "ESTO RECIBI")
        return recibe
    elif method == 'nuevo':
        print("AGREGANDO")
        data = {'usuario': usuario, 'email': email, 'password': password}
        recibe = asyncio.get_event_loop().run_until_complete(conectar(medula, 'nuevo_usuario', data))
        print(recibe, "ESTO RECIBI")
        return recibe
    elif method == 'cambio':
        print("MODIFICANDO")
        recibe = asyncio.get_event_loop().run_until_complete(conectar(medula, 'cambio_usuario', data))
        print(recibe, "ESTO RECIBI")
        return recibe
    else:
        print("ALGO MAS")

def actualizacion_internet():
    pass

def actualizacion_jovenclub():
    pass

def actualizacion_emby():
    pass

def actualizacion_filezilla():
    pass


async def conectar(url, command, data):
    try:
        async with websockets.connect(url) as ws:
            envia = json.dumps({'command': command, 'data': data})
            await ws.send(envia)
            recibe = await ws.recv()
            recibe = json.loads(recibe)
            return recibe
    except ConnectionRefusedError:
        print("EL SERVIDOR DENEGO LA CONEXION")
    except OSError:
        print("IP INALCANZABLE", OSError)
    except:
        print("NADA QUE DECIR")


""" if actualizacion_usuario('check', 'robinson5'):
    print("EL USUARIO EXISTE")
else:
    print("NO EXISTE, CREANDO")
    if actualizacion_usuario('nuevo', 'robinson5', 'manguero5@gmail.com', password='prueba123'):
        print("CREADO CON EXITO")
    else:
        print("FALLO LA CREACION") """