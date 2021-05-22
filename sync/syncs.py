from decouple import config
import asyncio
import websockets
import json

import websocket

#medula = config('MEDULA')
medula = 'ws://172.16.0.11:8000/ws/sync/'

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
        print("ALGO MAS")

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


def saludo(data):
    data = data['data']
    mensaje = data['mensaje']
    print(mensaje)

def respuesta(data):
    data = data['data']
    respuesta = data['existe']
    print(respuesta)

commands = {
        'saludo': saludo,
        'respuesta': respuesta,
    } 

def on_open(ws):
    print("SE CONECTO EL WS")
    command = 'saludo'
    data = {'identidad': 'cel1'}
    envia = json.dumps({'command': command, 'data': data})
    ws.send(envia)

def on_message(ws, data):
    data = json.loads(data)
    commands[data['command']](data)

def on_error(ws, error):
    print ("Se produjo un error: ", error)

def on_close(ws):
    print("SE CERRO EL WS")

websocket.setdefaulttimeout(5)
ws = websocket.WebSocketApp(medula, on_open=on_open, on_message=on_message, on_error=on_error, on_close=on_close)

ws.run_forever()