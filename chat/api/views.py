from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
import json

class ContactView(APIView):    
    
    def get(self, queryset=None, **kwargs):
        usuario = User.objects.get(username=self.kwargs.get('pk'))
        chats = usuario.chat_set.all()
        if chats:
            chats_list = []
            for chat in chats:
                contacto = chat.participantes.all().exclude(username=usuario.username)
                contacto = contacto.values('username')[0]
                new_chat = {'id': chat.id, 'contacto': contacto['username']}
                chats_list.append(new_chat)
                jsonData = json.dumps(chats_list)
            return Response(data={'chats_list': chats_list}, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)