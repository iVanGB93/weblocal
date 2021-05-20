from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import json
from django.utils import timezone
from django.core.mail import send_mail

from django.contrib.auth.models import User
from servicios.models import EstadoServicio

class SyncWSConsumer(WebsocketConsumer):
    def connect(self):
        print("CLIENTE CONECTADO")
        self.accept()
    
    def disconnect(self, close_code):
        print("CLIENTE DESCONECTADO", close_code)
        pass

    def check_usuario(self, data):
        existe = False
        if User.objects.filter(username=data['data']['usuario']).exists():
            existe = True
            self.responder(existe)
        else:
            self.responder(existe)

    def nuevo_usuario(self, data):
        correcto = False
        data = data['data']
        usuario = data['usuario']
        email = data['email']
        password = data['password']
        new_user = User(username=usuario, email=email)
        new_user.set_password(password)
        new_user.save()
        correcto = True
        self.responder(correcto)

    def cambio_usuario(self, data):
        correcto = False
        data = data['data']
        usuario_local = User.objects.get(username=data['usuario'])
        usuario_local.email = data['email']
        usuario_local.first_name = data['first_name']
        usuario_local.last_name = data['last_name']
        usuario_local.save()
        correcto = True
        self.responder(correcto)
    
    def check_servicio(self, data):
        correcto = True
        data = data['data']
        print(data)
        servicio_chequeo = data['servicio']
        usuario_local = User.objects.get(username=data['usuario'])
        servicio = EstadoServicio.objects.filter(usuario=usuario_local)
        print(servicio_chequeo)
        if servicio_chequeo == 'internet':
            for s in servicio:
                print(s.internet)
                if s.internet != data['servicio.internet']:
                    correcto = False
                    self.responder(correcto)
                elif s.int_time != data['servicio.int_time']:
                    correcto = False
                    self.responder(correcto)
                elif s.int_horas != data['servicio.int_horas']:
                    correcto = False
                    self.responder(correcto)
                elif s.int_tipo != data['servicio.int_tipo']:
                    correcto = False
                    self.responder(correcto)
                elif s.int_auto != data['servicio.int_auto']:
                    correcto = False
                    self.responder(correcto)
                else:
                    self.responder(correcto)
        elif servicio_chequeo == 'jovenclub':
            pass

        print(data, servicio.internet)

    def cambio_servicio(self, data):
        print("SERVICIO", data)


    commands = {
        'check_usuario': check_usuario,
        'nuevo_usuario': nuevo_usuario,
        'cambio_usuario': cambio_usuario,
        'check_servicio': check_servicio,
        'cambio_servicio': cambio_servicio,
    }  

    def receive(self, text_data):
        data = json.loads(text_data)
        print("LLEGO", data)
        self.commands[data['command']](self, data)
    
    def responder(self, data):
        data = json.dumps(data)
        self.send(data)