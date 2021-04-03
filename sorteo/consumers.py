from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import json
import random

from .models import Sorteo


class WSConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )        
        self.accept()
    
    # Receive message from WebSocket
    def receive(self, text_data):
        data = json.loads(text_data) 
        self.commands[data['command']](self, data)

    def participants(self, data):
        participants = Sorteo.objects.all()
        content = {
            'command': 'participants',
            'participants': self.participants_to_json(participants),
        }
        self.send_chat_message(content)
    
    def participants_to_json(self, participants):
        result = []
        for participant in participants:
            result.append(self.participant_to_json(participant))
        return result
    
    def participant_to_json(self, participant):
        result = []
        return {
            'usuario': participant.usuario.username,
            'code': participant.code,
            'eliminado': participant.eliminado,
            'servicio': participant.servicio
        }
        return result

    def roll(self, data):
        participants = Sorteo.objects.filter(eliminado=False)
        codes = []
        for p in participants:
            codes.append(p.code)
        if len(codes) > 1:
            if len(codes) == 2:
                code = random.choice(codes)
                selected = Sorteo.objects.get(code=code)
                selected.eliminado = True
                selected.save()
                ganador = Sorteo.objects.get(eliminado=False)
                content = {
                    'command': 'code',
                    'code': "El ganador es " + ganador.usuario.username + " " + ganador.servicio
                }
                self.send_chat_message(content)
            else:
                code = random.choice(codes)
                selected = Sorteo.objects.get(code=code)
                selected.eliminado = True
                selected.save()
                content = {
                    'command': 'code',
                    'code': "El eliminado es " + selected.usuario.username + " " + selected.servicio
                }
                self.send_chat_message(content)
        else:
            content = {
                'command': 'code',
                'code': 'Ya ha terminado el sorteo'
            }
            self.send_chat_message(content)

    commands = {
        'participants': participants,        
        'roll': roll,
    }

    def send_message(self, message):
        self.send(text_data=json.dumps(message))
    
    def send_chat_message(self, message): 
        # Send message to room group  
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,                
            }
        )
    
    # Receive message from room group
    def chat_message(self, event):
        message = event['message']        
        # Send message to WebSocket
        self.send(text_data=json.dumps(message))
    
    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )