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

from servicios.actions import *

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
    
    def put(self, request, **kwargs):
        respuesta = {'estado': False}
        user = self.kwargs.get('pk')
        usuario = User.objects.get(username=user)
        servicios = EstadoServicio.objects.get(usuario=usuario)
        request.data['usuario'] = usuario.id
        request.data['id'] = servicios.id
        serializer = ServiciosSerializer(servicios, data=request.data)
        if serializer.is_valid():
            serializer.update(servicios, serializer.validated_data)
            respuesta['estado'] = True
            respuesta['mensaje'] = 'Servicios actualizados con exito'
            return Response(status=status.HTTP_200_OK, data=respuesta)
        else:
            respuesta['mensaje'] = serializer.error
            return Response(status=status.HTTP_400_BAD_REQUEST, data=respuesta)

class InternetView(APIView):

    def get(self, queryset=None, **kwargs):
        user = self.kwargs.get('pk')
        usuario = User.objects.get(username=user)
        servicios = EstadoServicio.objects.get(usuario=usuario.id)
        servicios.internet = False
        servicios.int_time = None
        servicios.int_tipo = None
        servicios.int_horas = None
        servicios.sync = False
        servicios.save()
        return Response(status=status.HTTP_200_OK)

    def put(self, request, **kwargs):
        respuesta = {'estado': False}
        user = self.kwargs.get('pk')
        usuario = User.objects.get(username=user)
        tipo = request.data['tipo']
        contra = request.data['contra']
        duracion = request.data['duracion']
        horas = request.data['horas']
        velocidad = request.data['velocidad']
        result = comprar_internet(usuario, tipo, contra, duracion, horas, velocidad)
        if result['correcto']:
            respuesta['estado'] = True                
            respuesta['color_msg'] = 'success'                    
        respuesta['mensaje'] = result['mensaje']
        return Response(data=respuesta, status=status.HTTP_200_OK)

class JovenClubView(APIView):

    def put(self, request, **kwargs):
        respuesta = {'estado': False}
        user = self.kwargs.get('pk')
        result = comprar_jc(user)
        if result['correcto']:
            respuesta['estado'] = True
        respuesta['mensaje'] = result['mensaje']
        return Response(data=respuesta, status=status.HTTP_200_OK)

class EmbyView(APIView):

    def put(self, request, **kwargs):
        respuesta = {'estado': False}
        user = self.kwargs.get('pk')
        result = comprar_emby(user)
        if result['correcto']:
            respuesta['estado'] = True
        respuesta['mensaje'] = result['mensaje']
        return Response(data=respuesta, status=status.HTTP_200_OK)
        
class FileZillaView(APIView):

    def put(self, request, **kwargs):
        respuesta = {'estado': False}
        user = self.kwargs.get('pk')
        contra = request.data['contraseña']
        result = comprar_filezilla(user, contra)
        print(result)
        if result['correcto']:
            respuesta['estado'] = True
        respuesta['mensaje'] = result['mensaje']
        return Response(data=respuesta, status=status.HTTP_200_OK)
       

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
    
    def put(self, request, format=None, **kwargs):
        code = self.kwargs.get('pk')
        if Oper.objects.filter(code=code):
            oper = Oper.objects.get(code=code)
            oper.sync = True
            oper.save()
            return Response(status=status.HTTP_200_OK)
        usuario = User.objects.get(username=request.data['usuario'])
        if request.data['servicio'] == 'None':
            servicio = None
        else:
            servicio = request.data['servicio']
        if request.data['codRec'] == 'None':
            codRec = None
        else:
            codRec = request.data['codRec']
        if request.data['haciaDesde'] == 'None':
            haciaDesde = None
        else:
            haciaDesde = request.data['haciaDesde']
        oper = Oper(code=code, tipo=request.data['tipo'], usuario=usuario, servicio=servicio, codRec=codRec, cantidad=request.data['cantidad'], haciaDesde=haciaDesde, fecha=request.data['fecha'])
        oper.sync = True
        oper.save()
        return Response(status=status.HTTP_200_OK)

class RecargaView(APIView):

    def put(self, request, format=None, **kwargs):
        respuesta = {'estado': False}
        code = self.kwargs.get('pk')
        username = request.data['usuario']
        if Recarga.objects.filter(code=code):
            recarga = Recarga.objects.get(code=code)
            recarga.activa = False
            recarga.usuario = User.objects.get(username=username)
            recarga.fechaUso = timezone.now()
            recarga.sync = True
            recarga.save()
            respuesta['estado'] = True
            respuesta['mensaje'] = 'La recarga se guardo correctamente'
            return Response(status=status.HTTP_200_OK, data=respuesta)
        else:
            respuesta['mensaje'] = 'La recarga no se encontro'
            return Response(status=status.HTTP_200_OK, data=respuesta)

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
        