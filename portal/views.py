from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from users.models import Profile
from .forms import EditUserForm
from servicios.models import EstadoServicio, Oper
from servicios.actions import *

def index(request):
    return render(request, 'portal/index.html')

@login_required(login_url='/users/login/')
def dashboard(request):
    usuario = User.objects.get(username=request.user)
    perfil = Profile.objects.get(usuario=usuario)
    servicio = EstadoServicio.objects.get(usuario=usuario)
    content = {'usuario': usuario, 'perfil': perfil, 'servicio': servicio}
    return render(request, 'portal/dashboard.html', content)

@login_required(login_url='/users/login/')
def perfil(request):
    usuario = User.objects.get(username=request.user)
    if request.method == 'POST':        
        form = EditUserForm(request.POST)
        if form.is_valid():
            usuario = User.objects.get(username=request.user)
            usuario.email = request.POST['email']
            usuario.first_name = request.POST['first_name']
            usuario.last_name = request.POST['last_name']
            usuario.save()
            form = EditUserForm()
            mensaje = 'Perfil editado con éxito'
            content = {'mensaje': mensaje, 'form': form}
            return render(request, 'portal/perfil.html', content)
    else:
        form = EditUserForm()
        content = {'form': form}
        return render(request, 'portal/perfil.html', content)

@login_required(login_url='/users/login/')
def contra(request):
    if request.method == 'POST':
        usuario = User.objects.get(username=request.user)
        contra = request.POST['actual']
        if usuario.check_password(contra):
            if request.POST['nueva'] == request.POST['confirme']:
                if len(request.POST['nueva']) >= 8:
                    nueva = request.POST['nueva']
                    usuario.set_password(nueva)
                    usuario.save()
                    mensaje = 'Contraseña cambiada con éxito.'
                    content = {'mensaje': mensaje}
                    return render(request, 'portal/cambiarcontra.html', content)
                else:
                    mensaje = 'La contraseña debe tener al menos 8 caracteres.'
                    content = {'mensaje': mensaje}
                    return render(request, 'portal/cambiarcontra.html', content)
            else:
                mensaje = 'Las contraseñas nuevas no coinciden.'
                content = {'mensaje': mensaje}
                return render(request, 'portal/cambiarcontra.html', content)
        else:
            mensaje = 'Contraseña actual incorrecta.'
            content = {'mensaje': mensaje}
            return render(request, 'portal/cambiarcontra.html', content)
    else:
        return render(request, 'portal/cambiarcontra.html')

@login_required(login_url='/users/login/')
def internet(request):
    usuario = request.user
    perfil = Profile.objects.get(usuario=usuario)
    servicio = EstadoServicio.objects.get(usuario=usuario)
    if request.method == 'POST':
        tipo = request.POST['tipo']
        horas = request.POST['cantidad_horas']
        contra = request.POST['contra']
        if tipo != 'Seleccione el tipo':
            if usuario.check_password(contra):
                result = compra_internet(usuario, tipo, contra, horas)
                if result['correcto']:
                    mensaje = result['mensaje']
                    content = {'mensaje': mensaje, 'perfil': perfil, 'servicio': servicio}
                    return render(request, 'portal/internet.html', content)
                else:
                    mensaje = result['mensaje']
                    content = {'mensaje': mensaje, 'perfil': perfil, 'servicio': servicio}
                    return render(request, 'portal/internet.html', content)
            else:
                mensaje = 'Contraseña incorrecta.'
                content = {'mensaje': mensaje, 'perfil': perfil, 'servicio': servicio}
                return render(request, 'portal/internet.html', content)
        else:
            mensaje = 'Seleccione un tipo de internet'
            content = {'mensaje': mensaje, 'perfil': perfil, 'servicio': servicio}
            return render(request, 'portal/internet.html', content)         
    else:
        content = {'perfil': perfil, 'servicio': servicio} 
        return render(request, 'portal/internet.html', content)

@login_required(login_url='/users/login/')
def jovenclub(request):
    usuario = request.user
    perfil = Profile.objects.get(usuario=usuario)
    servicio = EstadoServicio.objects.get(usuario=usuario)
    if request.method == 'POST':
        contra = request.POST['contra']
        if usuario.check_password(contra):
            result = comprar_jc(usuario)
            if result['correcto']:
                mensaje = result['mensaje']
                content = {'mensaje': mensaje, 'perfil': perfil, 'servicio': servicio}
                return render(request, 'portal/jovenclub.html', content)
            else:
                mensaje = result['mensaje']
                content = {'mensaje': mensaje, 'perfil': perfil, 'servicio': servicio}
                return render(request, 'portal/jovenclub.html', content)
        else:
            mensaje = 'Contraseña incorrecta.'
            content = {'mensaje': mensaje, 'perfil': perfil, 'servicio': servicio}
            return render(request, 'portal/jovenclub.html', content)
    else:
        content = {'perfil': perfil, 'servicio': servicio} 
        return render(request, 'portal/jovenclub.html', content)

@login_required(login_url='/users/login/')
def emby(request):
    usuario = request.user
    perfil = Profile.objects.get(usuario=usuario)
    servicio = EstadoServicio.objects.get(usuario=usuario)
    if request.method == 'POST':
        contra = request.POST['contra']
        if usuario.check_password(contra):
            result = comprar_emby(usuario)
            if result['correcto']:
                mensaje = result['mensaje']
                content = {'mensaje': mensaje, 'perfil': perfil, 'servicio': servicio}
                return render(request, 'portal/emby.html', content)
            else:
                mensaje = result['mensaje']
                content = {'mensaje': mensaje, 'perfil': perfil, 'servicio': servicio}
                return render(request, 'portal/emby.html', content)
        else:
            mensaje = 'Contraseña incorrecta.'
            content = {'mensaje': mensaje, 'perfil': perfil, 'servicio': servicio}
            return render(request, 'portal/emby.html', content)
    else:
        content = {'perfil': perfil, 'servicio': servicio} 
        return render(request, 'portal/emby.html', content)

@login_required(login_url='/users/login/')
def filezilla(request):
    usuario = request.user
    perfil = Profile.objects.get(usuario=usuario)
    servicio = EstadoServicio.objects.get(usuario=usuario)
    if request.method == 'POST':
        contra = request.POST['contra']        
        if usuario.check_password(contra):                    
            result = comprar_filezilla(usuario, contra)
            if result['correcto']:
                mensaje = result['mensaje']
                content = {'mensaje': mensaje, 'perfil': perfil, 'servicio': servicio}
                return render(request, 'portal/filezilla.html', content)
            else:
                mensaje = result['mensaje']
                content = {'mensaje': mensaje, 'perfil': perfil, 'servicio': servicio}
                return render(request, 'portal/filezilla.html', content)
        else:
            mensaje = 'Contraseña incorrecta.'
            content = {'mensaje': mensaje, 'perfil': perfil, 'servicio': servicio}
            return render(request, 'portal/filezilla.html', content)
    else:
        content = {'perfil': perfil, 'servicio': servicio}  
        return render(request, 'portal/filezilla.html', content)

@login_required(login_url='/users/login/')
def recarga(request):
    usuario = request.user
    perfil = Profile.objects.get(usuario=usuario)
    if request.method == 'POST':
        code = request.POST['code']
        try:
            int(code)
            result = recargar(code, usuario)
            if result['correcto']:
                mensaje = result['mensaje']
                content = {'mensaje': mensaje, 'perfil': perfil}
                return render(request, 'portal/recarga.html', content)
            else:
                mensaje = result['mensaje']
                content = {'mensaje': mensaje, 'perfil': perfil}
                return render(request, 'portal/recarga.html', content)
        except ValueError:
            mensaje = "Solo escriba números"
            content = {'mensaje': mensaje, 'perfil': perfil}
            return render(request, 'portal/recarga.html', content)
    else:     
        content = {'perfil': perfil}  
        return render(request, 'portal/recarga.html', content)

@login_required(login_url='/users/login/')
def transferencia(request):
    usuario = request.user
    perfil = Profile.objects.get(usuario=usuario)
    if request.method == 'POST':
        hacia = request.POST['hacia']
        cantidad = request.POST['cantidad']
        try:
            cantidad = int(cantidad)
            result = transferir(usuario, hacia, cantidad)
            if result['correcto']:
                mensaje = result['mensaje']
                perfil = Profile.objects.get(usuario=usuario)
                content = {'mensaje': mensaje, 'perfil': perfil}
                return render(request, 'portal/transferencia.html', content)
            else:
                mensaje = result['mensaje']
                content = {'mensaje': mensaje, 'perfil': perfil}
                return render(request, 'portal/transferencia.html', content)
        except ValueError:
            mensaje = 'La cantidad es solo números'
            content = {'perfil': perfil, 'mensaje': mensaje}
            return render(request, 'portal/transferencia.html', content)
    else:
        content = {'perfil': perfil}
        return render(request, 'portal/transferencia.html', content)

@login_required(login_url='/users/login/')
def operaciones(request):
    usuario = request.user
    if User.objects.filter(username=usuario).exists():
        opers = Oper.objects.filter(usuario=usuario).order_by('-fecha')[:10]
        content = {'opers': opers}
        return render(request, 'portal/operaciones.html', content)
    else:
        mensaje = 'Usuario no existe'
        content = {'mensaje': mensaje}
        return render (request, 'portal/operaciones.html', content)