from servicios.models import Oper, Recarga, EstadoServicio
from users.models import Profile
from django.contrib.auth.models import User
from .serializers import OperSerializer, ServiciosSerializer
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.mail import send_mail
from django.utils import timezone
from datetime import datetime, timedelta
from decouple import config
import json

from servicios.actions import comprar_internet

class ServiciosView(APIView):    

    def get(self, queryset=None, **kwargs):
        user = self.kwargs.get('pk')
        if User.objects.filter(username=user).exists():
            usuario = User.objects.get(username=user)
            servicios = EstadoServicio.objects.get(usuario=usuario.id)         
            serializer = ServiciosSerializer(servicios)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

class InternetView(APIView):

    def get(self, queryset=None, **kwargs):        
        user = self.kwargs.get('pk')
        usuario = User.objects.get(username=user)
        return Response(status=status.HTTP_200_OK)

    def put(self, request, **kwargs):
        respuesta = {'estado': False}
        user = self.kwargs.get('pk')
        usuario = User.objects.get(username=user)
        tipo = request.data['tipo']
        contra = request.data['contra']
        duracion = request.data['duracion']
        horas = request.data['horas']
        result = comprar_internet(usuario, tipo, contra, duracion, horas)
        if result['correcto']:
            respuesta['estado'] = True                
            respuesta['color_msg'] = 'success'                    
        respuesta['mensaje'] = result['mensaje']
        return Response(data=respuesta, status=status.HTTP_200_OK)

class JovenClubView(APIView):

    def put(self, request, **kwargs):
        user = self.kwargs.get('pk')
        usuario = User.objects.get(username=user)
        profile = Profile.objects.get(usuario=usuario.id)
        servicio = EstadoServicio.objects.get(usuario=usuario.id)
        datos= request.data
        

class EmbyView(APIView):

    def put(self, request, **kwargs):
        user = self.kwargs.get('pk')
        usuario = User.objects.get(username=user)
        profile = Profile.objects.get(usuario=usuario.id)
        servicio = EstadoServicio.objects.get(usuario=usuario.id)
        datos= request.data
        
class FileZillaView(APIView):

    def put(self, request, **kwargs):
        user = self.kwargs.get('pk')
        usuario = User.objects.get(username=user)
        profile = Profile.objects.get(usuario=usuario.id)
        servicio = EstadoServicio.objects.get(usuario=usuario.id)
        datos= request.data
       

class OperView(APIView):  

    def get(self, request, format=None, **kwargs):
        username = self.kwargs.get('pk')
        if User.objects.filter(username=username).exists():
            usuario = User.objects.get(username=username)
            opers = Oper.objects.filter(usuario=usuario.id).order_by('-fecha')[:10]
            serializer = OperSerializer(opers, many=True)            
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

class RecargaView(APIView):

    def post(self, request, format=None, **kwargs):
        code = self.kwargs.get('pk')
        username = request.data['usuario']       
        

class TransferView(APIView):

    def get(self, request, format=None, **kwargs):
        username = self.kwargs.get('pk')       
        if User.objects.filter(username=username).exists():
            return Response(status=status.HTTP_200_OK)
        else:            
            return Response(status=status.HTTP_404_NOT_FOUND)
    
    def post(self, request, format=None, **kwargs):
        username = self.kwargs.get('pk')
        data = request.data
        usuario = data['usuario']
        cantidad = data['cantidad']
        envia = User.objects.get(username=username)
        recibe = User.objects.get(username=usuario)        
        enviaProfile = Profile.objects.get(usuario=envia.id)
        recibeProfile = Profile.objects.get(usuario=recibe.id)
        