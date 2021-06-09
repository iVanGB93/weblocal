from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.utils import timezone
from .models import Publicacion
from .forms import PublicacionForm

def tema_color(tema):
    if tema == "Emby":
        color = "success"
    elif tema == "Noticia":
        color = "warning"
    elif tema == "QbaRed":
        color = "info"
    elif tema == "Internet":
        color = "light"
    elif tema == "JovenClub":
        color = "primary"
    else:
        color = "danger"
    return color

def color_tema(color):
    if color == "success":
        tema = "Emby"
    elif color == "warning":
        tema = "Noticia"
    elif color == "info":
        tema = "QbaRed"
    elif color == "light":
        tema = "Internet"
    elif color == "primary":
        tema = "JovenClub"
    else:
        tema = "FileZilla"
    return tema

def index(request, pk):
    publicaciones = Publicacion.objects.filter(tema=pk).order_by('-fecha')
    todas = Publicacion.objects.all().order_by('-fecha')[:20]
    color = tema_color(pk)
    tema = pk
    data = {'publicaciones': publicaciones, 'todas': todas, 'color': color, 'tema': tema}
    return render(request, 'forum/index.html', data)

def detalles(request, tema, pk):
    publicacion = Publicacion.objects.get(id=pk)
    if request.user != publicacion.autor:
        publicacion.visitas = publicacion.visitas + 1
        publicacion.save()
    color = tema_color(tema)
    data = {'p': publicacion, 'color': color, 'tema': tema}
    return render(request, 'forum/detalles.html', data)

def crear(request, tema):
    color = tema_color(tema)
    content = {'tema': tema, 'color': color}
    if request.method == 'POST':        
        usuario = User.objects.get(username=request.user)
        tema = request.POST['tema']
        titulo = request.POST['titulo']
        if Publicacion.objects.filter(titulo=titulo).exists():
            mensaje = 'Existe una publicación con este título'
            content['mensaje'] =  mensaje
            return render(request, 'forum/crear.html', content)
        contenido = request.POST['contenido']       
        nueva = Publicacion(autor=usuario, tema=tema, titulo=titulo, contenido=contenido)        
        if request.POST.get('online'):
            nueva.online = True
        if request.FILES.get('imagen1'):
            nueva.imagen1 = request.FILES['imagen1']
        if request.FILES.get('imagen2'):
            nueva.imagen2 = request.FILES['imagen2']       
        if request.FILES.get('imagen3'):
            nueva.imagen3 = request.FILES['imagen3']
        nueva.save()        
        mensaje = 'Artículo publicado con éxito'
        content['p'] = nueva
        content['tema'] = tema
        content['mensaje'] = mensaje    
        return render(request, 'forum/detalles.html', content)
    else:
        return render(request, 'forum/crear.html', content)

def editar(request, tema, pk):
    publicacion = Publicacion.objects.get(id=pk)
    color = tema_color(tema)
    content = {'p': publicacion, 'tema': tema, 'color': color}
    if request.method == 'POST':
        tema = request.POST['tema']
        publicacion.tema = tema
        if request.POST['titulo'] != '':
            titulo = request.POST['titulo']
            if titulo != publicacion.titulo:
                if Publicacion.objects.filter(titulo=titulo).exists():
                    mensaje = 'Existe una publicación con este título'
                    content['mensaje'] =  mensaje
                    return render(request, 'forum/editar.html', content)
            publicacion.titulo = titulo
        if request.POST['contenido'] != '':
            publicacion.contenido = request.POST['contenido']
        if request.POST.get('online'):
            publicacion.online = True
        else:
            publicacion.online = False
        if request.FILES.get('imagen1'):
            publicacion.imagen1 = request.FILES['imagen1']
        if request.FILES.get('imagen2'):
            publicacion.imagen2 = request.FILES['imagen2']       
        if request.FILES.get('imagen3'):
            publicacion.imagen3 = request.FILES['imagen3']
        publicacion.fecha = timezone.now()
        publicacion.save()    
        mensaje = 'Publicación modificada con éxito'
        content = {'p': publicacion, 'tema': tema, 'color': color}
        content['mensaje'] =  mensaje    
        return redirect('forum:detalles', tema, pk)
    else:
        return render(request, 'forum/editar.html', content) 

def eliminar(request, tema, pk):
    publicacion = Publicacion.objects.get(id=pk)
    color = tema_color(tema)
    content = {'p': publicacion, 'tema': tema, 'color': color}
    if request.method == 'POST':
        publicacion.delete()
        publicaciones = Publicacion.objects.filter(tema=pk).order_by('-fecha')
        todas = Publicacion.objects.all().order_by('-fecha')[:20]
        data = {'publicaciones': publicaciones, 'todas': todas, 'color': color, 'tema': tema}
        return redirect('forum:index', tema)
    else:
        return render(request, 'forum/eliminar.html', content)