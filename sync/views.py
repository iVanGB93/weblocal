from typing import ContextManager
from django.shortcuts import render, resolve_url
from rest_framework import serializers
from .syncs import actualizacion_usuario, actualizacion_servicio, actualizacion_perfil

from servicios.api.serializers import ServiciosSerializer
from users.api.serializers import ProfileSerializer
from django.contrib.auth.models import User
from servicios.models import EstadoServicio
from users.models import Profile

def control(request):
    usuarios = User.objects.all()
    perfiles = Profile.objects.all()
    servicios = EstadoServicio.objects.all()
    if request.method == 'POST':
        content = {'usuarios': usuarios, 'perfiles': perfiles, 'servicios': servicios}
        return render(request, 'sync/index.html', content)
    else:
        content = {'usuarios': usuarios, 'perfiles': perfiles, 'servicios': servicios}
        return render(request, 'sync/index.html', content)

def control_usuario(request, id):
    usuarios = User.objects.all()
    perfiles = Profile.objects.all()
    servicios = EstadoServicio.objects.all()
    if request.method == 'POST':
        usuario = User.objects.get(id=id)        
        respuesta = actualizacion_usuario('check', usuario.username)
        if respuesta['conexion']:
            if respuesta['estado']:   
                mensaje = respuesta['mensaje']
                content = {'usuarios': usuarios, 'perfiles': perfiles, 'servicios': servicios, 'mensaje': mensaje}
                return render(request, 'sync/index.html', content)
            else:
                mensaje = "Usuario NO existe en internet."
                content = {'usuario': usuario.username, 'mensaje': mensaje, 'id': id}
                return render(request, 'sync/crear_eliminar_usuario.html', content)
        else:
            mensaje = respuesta['mensaje']
            content = {'usuarios': usuarios, 'perfiles': perfiles, 'servicios': servicios, 'mensaje': mensaje}
            return render(request, 'sync/index.html', content)
    else:
        mensaje = "Algo salio mal."
        content = {'usuarios': usuarios, 'perfiles': perfiles, 'servicios': servicios, 'mensaje': mensaje}
        return render(request, 'sync/index.html', content)
    

def crear_eliminar_usuario(request, id):
    usuario = User.objects.get(id=id)
    usuarios = User.objects.all()
    perfiles = Profile.objects.all()
    servicios = EstadoServicio.objects.all()
    if request.method == 'POST':
        if request.POST['respuesta'] == 'crear':
            result = actualizacion_usuario('nuevo', usuario.username, usuario.email, usuario.password)
            if result:
                mensaje = "Se creo el usuario con éxito."
                content = {'usuarios': usuarios, 'perfiles': perfiles, 'servicios': servicios, 'mensaje': mensaje}
                return render(request, 'sync/index.html', content)
            else:
                mensaje = "Ocurrio algun error en la creación."
                content = {'usuarios': usuarios, 'perfiles': perfiles, 'servicios': servicios, 'mensaje': mensaje}
                return render(request, 'sync/index.html', content)
        elif request.POST['respuesta'] == 'eliminar':
            usuario.delete()
            mensaje = "Se eliminó definitivamente el usuario."
            content = {'usuarios': usuarios, 'perfiles': perfiles, 'servicios': servicios, 'mensaje': mensaje}
            return render(request, 'sync/index.html', content)
    else:
        mensaje = "Algo salio mal."
        content = {'usuarios': usuarios, 'perfiles': perfiles, 'servicios': servicios, 'mensaje': mensaje}
        return render(request, 'sync/index.html', content)

def control_perfil(request, id):
    usuarios = User.objects.all()
    perfiles = Profile.objects.all()
    servicios = EstadoServicio.objects.all()
    if request.method == 'POST':
        usuario = User.objects.get(id=id)   
        profile = Profile.objects.get(usuario=usuario)
        serializer = ProfileSerializer(profile)
        data = serializer.data
        respuesta = actualizacion_perfil('check', usuario.username, data)
        if respuesta['conexion']:
            if respuesta['estado']:   
                profile.sync = True
                profile.save()
                perfiles = Profile.objects.all()
                mensaje = respuesta['mensaje']
                content = {'usuarios': usuarios, 'perfiles': perfiles, 'servicios': servicios, 'mensaje': mensaje}
                return render(request, 'sync/index.html', content)
            else:
                mensaje = respuesta['mensaje']
                content = {'usuario': usuario.username, 'mensaje': mensaje, 'id': id}
                return render(request, 'sync/actualizar_perfil.html', content)
        else:
            mensaje = respuesta['mensaje']
            content = {'usuarios': usuarios, 'perfiles': perfiles, 'servicios': servicios, 'mensaje': mensaje}
            return render(request, 'sync/index.html', content)
    else:
        mensaje = "Algo salio mal."
        content = {'usuarios': usuarios, 'perfiles': perfiles, 'servicios': servicios, 'mensaje': mensaje}
        return render(request, 'sync/index.html', content)

def actualizar_perfil(request, id):
    usuario = User.objects.get(id=id)
    usuarios = User.objects.all()
    perfiles = Profile.objects.all()
    servicios = EstadoServicio.objects.all()
    if request.method == 'POST':
        if request.POST['respuesta'] == 'local':
            profile = Profile.objects.get(usuario=usuario)
            serializer = ProfileSerializer(profile)
            data = serializer.data
            respuesta = actualizacion_perfil('cambio', usuario.username, data)
            if respuesta['conexion']:
                if respuesta['estado']:
                    mensaje = respuesta['mensaje']
                    perfiles = Profile.objects.all()
                    content = {'usuarios': usuarios, 'perfiles': perfiles, 'servicios': servicios, 'mensaje': mensaje}
                    return render(request, 'sync/index.html', content)
                else:
                    mensaje = respuesta['mensaje']
                    content = {'usuarios': usuarios, 'perfiles': perfiles, 'servicios': servicios, 'mensaje': mensaje}
                    return render(request, 'sync/index.html', content)
            else:
                mensaje = respuesta['mensaje']
                content = {'usuarios': usuarios, 'perfiles': perfiles, 'servicios': servicios, 'mensaje': mensaje}
                return render(request, 'sync/index.html', content)
        elif request.POST['respuesta'] == 'remoto':
            pass
    else:
        mensaje = "Algo salio mal."
        content = {'usuarios': usuarios, 'perfiles': perfiles, 'servicios': servicios, 'mensaje': mensaje}
        return render(request, 'sync/index.html', content)


def control_servicio(request, id):
    usuario = User.objects.get(id=id)
    usuarios = User.objects.all()
    perfiles = Profile.objects.all()
    servicios = EstadoServicio.objects.all()
    servicio = EstadoServicio.objects.get(usuario=usuario)
    if request.method == 'POST':
        if request.POST['action'] == 'check':            
            serializer = ServiciosSerializer(servicio)
            data=serializer.data
            respuesta = actualizacion_servicio('check', usuario.username, 'internet', data)
            if respuesta['conexion']:
                if respuesta['estado']: 
                    mensaje = "Servicio sincronizado."
                    content = {'usuarios': usuarios, 'perfiles': perfiles, 'servicios': servicios, 'mensaje': mensaje}
                    return render(request, 'sync/index.html', content)
                else:
                    servicio.sync = False
                    servicio.save()
                    servicios = EstadoServicio.objects.all()
                    mensaje = "El servicio no está sincronizado."
                    content = {'usuarios': usuarios, 'perfiles': perfiles, 'servicios': servicios, 'mensaje': mensaje}
                    return render(request, 'sync/index.html', content)
            else:
                mensaje = respuesta['mensaje']
                content = {'usuarios': usuarios, 'perfiles': perfiles, 'servicios': servicios, 'mensaje': mensaje}
                return render(request, 'sync/index.html', content)
        if request.POST['action'] == 'cambiar':
            serializer = ServiciosSerializer(servicio)
            data=serializer.data
            respuesta = actualizacion_servicio('guardar', usuario.username, 'internet', data)
            if respuesta['conexion']:
                if respuesta['estado']:
                    servicio.sync = True
                    servicio.save()
                    servicios = EstadoServicio.objects.all()
                    mensaje = "Se sincronizó el servicio con éxito."
                    content = {'usuarios': usuarios, 'perfiles': perfiles, 'servicios': servicios, 'mensaje': mensaje}
                    return render(request, 'sync/index.html', content)
                else:
                    mensaje = respuesta['mensaje']
                    content = {'usuarios': usuarios, 'perfiles': perfiles, 'servicios': servicios, 'mensaje': mensaje}
                    return render(request, 'sync/index.html', content)
            else:
                mensaje = respuesta['mensaje']
                content = {'usuarios': usuarios, 'perfiles': perfiles, 'servicios': servicios, 'mensaje': mensaje}
                return render(request, 'sync/index.html', content)
    else:
        mensaje = "Algo salio mal."
        content = {'usuarios': usuarios, 'perfiles': perfiles, 'servicios': servicios, 'mensaje': mensaje}
        return render(request, 'sync/index.html', content)