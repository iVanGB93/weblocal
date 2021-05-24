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

def actualizacion_usuario(accion, usuario, data):
    data['usuario'] = usuario
    recibe = get_or_create_eventloop().run_until_complete(conectar(medula, accion, data))
    return recibe

def actualizacion_perfil(accion, usuario, data):
    data['usuario'] = usuario
    recibe = get_or_create_eventloop().run_until_complete(conectar(medula, accion, data))
    return recibe
   

def actualizacion_servicio(accion, usuario, servicio, data):
    usuario = str(usuario)
    data['usuario'] = usuario
    data['servicio'] = servicio
    recibe = get_or_create_eventloop().run_until_complete(conectar(medula, accion, data))
    return recibe

async def conectar(url, command, data):
    respuesta = {'conexion': False, 'estado': False}
    try:
        async with websockets.connect(url) as ws:
            while True:
                envia = json.dumps({'command': command, 'data': data})
                await ws.send(envia)
                recibe = await ws.recv()
                recibe = json.loads(recibe)
                respuesta['estado'] = recibe['estado']
                respuesta['mensaje'] = recibe['mensaje']
                respuesta['conexion'] = True
                return respuesta
    except ConnectionRefusedError:
        print("EL SERVIDOR REMOTO DENEGO LA CONEXION")
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
