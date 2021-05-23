from decouple import config
import asyncio
import websockets
import json


#medula = config('MEDULA')
medula = 'ws://127.0.0.1:8080/ws/sync/'

def get_or_create_eventloop():
    try:
        return asyncio.get_event_loop()
    except RuntimeError as ex:
        if "There is no current event loop in thread" in str(ex):
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            return asyncio.get_event_loop()

def actualizacion_usuario(method, usuario, email=None, password=None, data=None):
    if method == 'check':
        print("CHECKING")
        data = {'usuario': usuario}
        recibe = get_or_create_eventloop().run_until_complete(conectar(medula, 'check_usuario', data))
        return recibe
    elif method == 'nuevo':
        print("AGREGANDO")
        data = {'usuario': usuario, 'email': email, 'password': password}
        recibe = get_or_create_eventloop().run_until_complete(conectar(medula, 'nuevo_usuario', data))
        return recibe
    elif method == 'cambio':
        print("MODIFICANDO")
        recibe = get_or_create_eventloop().run_until_complete(conectar(medula, 'cambio_usuario', data))
        return recibe
    else:
        print("ALGO MAL ACTUALIZACION")

def actualizacion_perfil(method, usuario, data):
    if method == 'check':
        print("CHECKING")
        data['usuario'] = usuario
        recibe = get_or_create_eventloop().run_until_complete(conectar(medula, 'check_perfil', data))
        return recibe
    if method == 'cambio':
        print("MODIFICANDO")
        data['usuario'] = usuario
        recibe = get_or_create_eventloop().run_until_complete(conectar(medula, 'cambio_perfil', data))
        return recibe
    else:
        print("ALGO MAL ACTUALIZACION")

def actualizacion_servicio(method, usuario, servicio, data):
    if method == 'check':
        print("CHECKING")
        usuario = str(usuario)
        data['usuario'] = usuario
        data['servicio'] = servicio
        recibe = get_or_create_eventloop().run_until_complete(conectar(medula, 'check_servicio', data))
        return recibe
    if method == 'cambio':
        print("MODIFICANDO")
        usuario = str(usuario)
        data['usuario'] = usuario
        data['servicio'] = servicio
        recibe = get_or_create_eventloop().run_until_complete(conectar(medula, 'cambio_servicio', data))
        return recibe
    if method == 'guardar':
        print("GUARDANDO")
        usuario = str(usuario)
        data['usuario'] = usuario
        recibe = get_or_create_eventloop().run_until_complete(conectar(medula, 'guardar_servicio', data))
        return recibe
    else:
        print("ALGO MAL ACTUALIZACION")

async def conectar(url, command, data):
    respuesta = {'conexion': False, 'estado': False}
    try:
        async with websockets.connect(url) as ws:
            envia = json.dumps({'command': command, 'data': data})
            await ws.send(envia)
            recibe = await ws.recv()
            recibe = json.loads(recibe)
            respuesta['estado'] = recibe['estado']
            respuesta['mensaje'] = recibe['mensaje']
            respuesta['conexion'] = True
            return respuesta
    except ConnectionRefusedError:
        print("EL SERVIDOR DENEGO LA CONEXION")
        respuesta['mensaje'] = 'EL SERVIDOR DENEGO LA CONEXION'
        return respuesta
    except OSError:
        print("IP INALCANZABLE", OSError)
        respuesta['mensaje'] = f'IP INALCANZABLE { OSError }'
        return respuesta
    except:
        print("NADA QUE DECIR, SOLO PROBLEMAS")
        respuesta['mensaje'] = 'NADA QUE DECIR, SOLO PROBLEMAS'
        return respuesta