from django.shortcuts import render
from .models import Publicacion


def index(request):
    publicaciones = Publicacion.objects.all().order_by('-fecha')  
    data = {'publicaciones': publicaciones}
    return render(request, 'forum/index.html', data)

def detalles(request, pk):
    publicacion = Publicacion.objects.filter(id=pk)
    for p in publicacion:
        if p.tema == "Emby":
            color = "success"
        if p.tema == "Sorteo":
            color = "primary"
        if p.tema == "QbaRed":
            color = "danger"
        if p.tema == "emby":
            color = "success"
        else:
            color = "danger"
    data = {'publicacion': publicacion, 'color': color}
    return render(request, 'forum/detalles.html', data)
