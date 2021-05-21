from re import T
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import json
from django.utils import timezone
from django.core.mail import send_mail

from django.contrib.auth.models import User
from servicios.models import EstadoServicio

class SyncWSConsumer(WebsocketConsumer):
    def connect(self):
        #self.room_name
        self.accept()
        """ usuario = self.scope['user']
        if usuario.is_authenticated:
            print(f"CLIENTE { usuario } CONECTADO")
            
        else:
            print("CONEXION DENEGADA") """
    
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
        servicio_chequeo = data['servicio']
        usuario_local = User.objects.get(username=data['usuario'])
        servicio = EstadoServicio.objects.filter(usuario=usuario_local)
        if servicio_chequeo == 'internet':
            for s in servicio:
                if s.internet != data['internet']:
                    correcto = False
                    self.responder(correcto)                
                elif s.int_horas != data['int_horas']:
                    correcto = False
                    self.responder(correcto)
                elif s.int_tipo != data['int_tipo']:
                    correcto = False
                    self.responder(correcto)
                elif s.int_auto != data['int_auto']:
                    correcto = False
                    self.responder(correcto)
                else:
                    self.responder(correcto)
        elif servicio_chequeo == 'jovenclub':
            for s in servicio:
                if s.jc != data['jc']:
                    correcto = False
                    self.responder(correcto)                
                elif s.jc_auto != data['jc_auto']:
                    correcto = False
                    self.responder(correcto)
                else:
                    self.responder(correcto)
        elif servicio_chequeo == 'emby':
            for s in servicio:
                if s.emby != data['emby']:
                    correcto = False
                    self.responder(correcto)                
                elif s.emby_id != data['emby_id']:
                    correcto = False
                    self.responder(correcto)
                elif s.emby_auto != data['emby_auto']:
                    correcto = False
                    self.responder(correcto)
                else:
                    self.responder(correcto)
        elif servicio_chequeo == 'filezilla':
            for s in servicio:
                if s.ftp != data['ftp']:
                    correcto = False
                    self.responder(correcto)               
                elif s.ftp_auto != data['ftp_auto']:
                    correcto = False
                    self.responder(correcto)
                else:
                    self.responder(correcto)

    def guardar_servicio(self, data):
        correcto = True
        data = data['data']        
        usuario_local = User.objects.get(username=data['usuario'])
        servicio = EstadoServicio.objects.filter(usuario=usuario_local)
        for s in servicio:
            s.internet = data['internet']                                  
            s.int_horas = data['int_horas']
            s.int_time = data['int_time']
            s.int_tipo = data['int_tipo']
            s.int_auto = data['int_auto']                   
            s.jc = data['jc']
            s.jc_time = data['jc_time']            
            s.jc_auto = data['jc_auto']          
            s.emby = data['emby']             
            s.emby_id = data['emby_id']
            s.emby_time = data['emby_time']
            s.emby_auto != data['emby_auto']
            s.ftp = data['ftp']              
            s.ftp_auto = data['ftp_auto']
            s.ftp_time = data['ftp_time']
            s.sync = True
            s.save()
        self.responder(correcto)

    def cambio_servicio(self, data):
        correcto = False
        data = data['data']
        servicio_cambio = data['servicio']
        usuario_local = User.objects.get(username=data['usuario'])
        servicio = EstadoServicio.objects.filter(usuario=usuario_local)
        if servicio_cambio == 'internet':
            for s in servicio:
                s.internet = data['internet']                                   
                s.int_horas = data['int_horas']                  
                s.int_tipo = data['int_tipo']
                s.int_time = data['int_time']                   
                s.int_auto = data['int_auto']
                s.save()
            correcto = True
            self.responder(correcto)
        elif servicio_cambio == 'jovenclub':
            for s in servicio:
                s.jc = data['jc']                                   
                s.jc_time = data['jc_time']                   
                s.jc_auto = data['jc_auto']
                s.save()
            correcto = True
            self.responder(correcto)
        elif servicio_cambio == 'emby':
            for s in servicio:
                s.emby = data['emby']                                   
                s.emby_time = data['emby_time']                   
                s.emby_id = data['emby_id']                   
                s.emby_auto = data['emby_auto']
                s.save()
            correcto = True
            self.responder(correcto)
        elif servicio_cambio == 'filezilla':
            for s in servicio:
                s.ftp = data['ftp']                                   
                s.ftp_time = data['ftp_time']                   
                s.ftp_auto = data['ftp_auto']
                s.save()
            correcto = True
            self.responder(correcto)

    commands = {
        'check_usuario': check_usuario,
        'nuevo_usuario': nuevo_usuario,
        'cambio_usuario': cambio_usuario,
        'check_servicio': check_servicio,
        'guardar_servicio': guardar_servicio,
        'cambio_servicio': cambio_servicio,
    }  

    def receive(self, text_data):
        data = json.loads(text_data)
        self.commands[data['command']](self, data)
    
    def responder(self, data):
        data = json.dumps(data)
        self.send(data)