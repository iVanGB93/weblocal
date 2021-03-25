from users.models import Profile, Notificacion
from django.contrib.auth.models import User
from .serializers import ProfileSerializer, UserSerializer
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status


class ProfileView(APIView):

    def get(self, queryset=None, **kwargs):
        user = self.kwargs.get('pk') 
        if User.objects.filter(username=user).exists():       
            usuario = User.objects.get(username=user)                               
            profile = Profile.objects.get(usuario=usuario.id)            
            serializer = ProfileSerializer(profile)            
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

class UserView(APIView):

    def get(self, queryset=None, **kwargs):
        user = self.kwargs.get('pk')
        if User.objects.filter(username=user).exists():
            usuario = User.objects.get(username=user)
            serializer = UserSerializer(usuario)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, **kwargs):
        user = self.kwargs.get('pk')
        datos = request.data
        if User.objects.filter(username=user).exists():
            usuario = User.objects.get(username=user)
            usuario.first_name = datos['first_name']
            usuario.email = datos['email']
            usuario.last_name = datos['last_name']
            usuario.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

class EmailCheckView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, queryset=None, **kwargs):
        email = self.kwargs.get('email')
        print(email)
        if User.objects.filter(email=email).exists():
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)