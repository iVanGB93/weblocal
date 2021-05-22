from typing import ContextManager
from django.shortcuts import render
from .syncs import actualizacion_usuario, actualizacion_servicio

from servicios.api.serializers import ServiciosSerializer
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
    if request.method == 'POST':
        usuario = User.objects.get(id=id)
        usuarios = User.objects.all()
        perfiles = Profile.objects.all()
        servicios = EstadoServicio.objects.all()
        if actualizacion_usuario('check', usuario.username):    
            mensaje = "Usuario existe."
            content = {'usuarios': usuarios, 'perfiles': perfiles, 'servicios': servicios, 'mensaje': mensaje}
            return render(request, 'sync/index.html', content)
        else:
            mensaje = "Usuario NO existe en internet."
            content = {'usuario': usuario.username, 'mensaje': mensaje, 'id': id}
            return render(request, 'sync/crear_eliminar_usuario.html', content)
    usuarios = User.objects.all()
    perfiles = Profile.objects.all()
    servicios = EstadoServicio.objects.all()
    content = {'usuarios': usuarios, 'perfiles': perfiles, 'servicios': servicios}
    return render(request, 'sync/index.html', content)

def crear_eliminar(request, id):
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

def control_servicio(request, id):
    usuario = User.objects.get(id=id)
    usuarios = User.objects.all()
    perfiles = Profile.objects.all()
    servicios = EstadoServicio.objects.all()
    if request.method == 'POST':
        if request.POST['action'] == 'check':            
            servicio = EstadoServicio.objects.get(usuario=usuario)
            serializer = ServiciosSerializer(servicio)
            data=serializer.data
            if actualizacion_servicio('check', usuario.username, 'internet', data):    
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
        if request.POST['action'] == 'cambiar':
            servicio = EstadoServicio.objects.get(usuario=usuario)
            serializer = ServiciosSerializer(servicio)
            data=serializer.data
            if actualizacion_servicio('guardar', usuario.username, 'internet', data):
                servicio.sync = True
                servicio.save()
                servicios = EstadoServicio.objects.all()
                mensaje = "Se sincronizó el servicio con éxito."
                content = {'usuarios': usuarios, 'perfiles': perfiles, 'servicios': servicios, 'mensaje': mensaje}
                return render(request, 'sync/index.html', content)
            else:
                mensaje = "Ocurrió algún error."
                content = {'usuarios': usuarios, 'perfiles': perfiles, 'servicios': servicios, 'mensaje': mensaje}
                return render(request, 'sync/index.html', content)