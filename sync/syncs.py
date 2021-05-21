from decouple import config
import asyncio
import websockets
import json


#medula = config('MEDULA')
medula = 'ws://172.16.0.11:8000/ws/sync/'


async def actualizacion_usuario(method, usuario, email=None, password=None, data=None):
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

async def actualizacion_servicio(method, usuario, servicio, data):
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
    recibe = False
    try:
        async with websockets.connect(url) as ws:
            envia = json.dumps({'command': command, 'data': data})
            await ws.send(envia)
            recibe = await ws.recv()
            recibe = json.loads(recibe)
            return recibe
    except ConnectionRefusedError:
        print("EL SERVIDOR DENEGO LA CONEXION")
        return recibe
    except OSError:
        print("IP INALCANZABLE", OSError)
        return recibe
    except:
        print("NADA QUE DECIR, SOLO PROBLEMAS")
        return recibe