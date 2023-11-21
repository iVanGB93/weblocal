from django.shortcuts import render
from sync.scheduler import get_or_create_conexion_status

def index(request):
    content = {'local': False}
    conexion = get_or_create_conexion_status()
    if hasattr(conexion, 'ip_online'):
        content['local'] = True
    return render(request, 'web/index.html', content)

def ts(request):
    content = {'local': False}
    conexion = get_or_create_conexion_status()
    if hasattr(conexion, 'ip_online'):
        content['local'] = True
    return render(request, 'web/ts.html', content)

def ftp(request):
    return render(request, 'web/ftp.html')

def emby(request):
    content = {'local': False}
    conexion = get_or_create_conexion_status()
    if hasattr(conexion, 'ip_online'):
        content['local'] = True
    return render(request, 'web/emby.html', content)

def jc(request):
    return render(request, 'web/jc.html')

def axie(request):
    return render(request, 'web/axie.html')
