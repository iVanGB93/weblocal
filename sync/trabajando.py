from decouple import config
import asyncio
import websockets
import json


medula = config('MEDULA')
medula = 'ws://127.0.0.1:8000/ws/sync/'

def actualizacion_usuario(method, usuario, email=None, password=None, data=None):
    if method == 'check':
        print("CHECKING")
        data = {'usuario': usuario}
        recibe = asyncio.get_event_loop().run_until_complete(conectar(medula, 'check_usuario', data))
        return recibe
    elif method == 'nuevo':
        print("AGREGANDO")
        data = {'usuario': usuario, 'email': email, 'password': password}
        recibe = asyncio.get_event_loop().run_until_complete(conectar(medula, 'nuevo_usuario', data))
        return recibe
    elif method == 'cambio':
        print("MODIFICANDO")
        recibe = asyncio.get_event_loop().run_until_complete(conectar(medula, 'cambio_usuario', data))
        return recibe
    else:
        print("ALGO MAS")

def actualizacion_servicio(method, usuario, servicio, data):
    if method == 'check':
        print("CHECKING")
        data['usuario'] = usuario
        data['servicio'] = servicio
        recibe = asyncio.get_event_loop().run_until_complete(conectar(medula, 'check_servicio', data))
        return recibe
    if method == 'cambio':
        print("MODIFICANDO")
        data['usuario'] = usuario
        data['servicio'] = servicio
        recibe = asyncio.get_event_loop().run_until_complete(conectar(medula, 'cambio_servicio', data))
        return recibe
    
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

data={'id': 1, 'internet': True, 'int_time': None, 'int_horas': 5, 'int_tipo': 'internetMensual',
 'int_auto': True, 'emby': False, 'emby_time': None, 'emby_id': None, 'emby_auto': False, 'jc': False, 
 'jc_time': '2021-06-15 19:45:31+00:00', 'jc_auto': True, 'ftp': True, 'ftp_time': '2021-06-14T16:53:36-04:00', 
 'ftp_auto': True}
print(actualizacion_servicio('check', 'iVan', 'filezilla', data))
