from django.contrib.auth.models import User
from .models import Sorteo
from servicios.models import Oper
from django.core.mail import send_mail
from django.utils import timezone
from .forms import CodeForm
from django.shortcuts import render


def index(request):
    if request.method == 'POST':
        form = CodeForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            if Oper.objects.filter(code=code).exists():
                oper = Oper.objects.get(code=code)
                ahora = timezone.now()
                if oper.fecha.month == ahora.month:
                    if Sorteo.objects.filter(code=code).exists():
                        form = CodeForm()
                        content = {
                            'form': form,
                            'message': 'Código usado'
                        }
                        return render(request, 'sorteo/index.html', content)
                    else:
                        if oper.tipo == "PAGO":
                            if oper.servicio == "internetHoras":
                                if oper.cantidad >= 100: 
                                    participacion = Sorteo(usuario=oper.usuario, code=code, servicio=oper.servicio)
                                    participacion.save()
                                    usuario = User.objects.get(username=oper.usuario)
                                    send_mail('Sorteo QbaRed', f'Usted esta participando en el sorteo de QbaRed con el código {code}, obtenido por el servicio {oper.servicio}. Suerte!!!', 'RedCentroHabanaCuba@gmail.com', [usuario.email])
                                    send_mail('Sorteo QbaRed', f'Se registro {usuario.username} con  el código {code}, obtenido por el servicio {oper.servicio}.', 'RedCentroHabanaCuba@gmail.com', ['ivanguachbeltran@gmail.com'])
                                    form = CodeForm()
                                    content = {
                                        'form': form,
                                        'message': 'Se ha agregado su participación',
                                        'success': 'success'
                                    }
                                    return render(request, 'sorteo/index.html', content)
                                else:
                                    form = CodeForm()
                                    content = {
                                        'form': form,
                                        'message': 'Código solo de pago de 10 horas o más'
                                    }
                                    return render(request, 'sorteo/index.html', content)                           
                            participacion = Sorteo(usuario=oper.usuario, code=code, servicio=oper.servicio)
                            participacion.save()
                            usuario = User.objects.get(username=oper.usuario)
                            send_mail('Sorteo QbaRed', f'Usted esta participando en el sorteo de QbaRed con el código {code}, obtenido por el servicio {oper.servicio}. Suerte!!!', 'RedCentroHabanaCuba@gmail.com', [usuario.email])
                            send_mail('Sorteo QbaRed', f'Se registro {usuario.username} con  el código {code}, obtenido por el servicio {oper.servicio}.', 'RedCentroHabanaCuba@gmail.com', ['ivanguachbeltran@gmail.com'])
                            form = CodeForm()
                            content = {
                                'form': form,
                                'message': 'Se ha agregado su participación',
                                'success': 'success'
                            }
                            return render(request, 'sorteo/index.html', content)
                        else:
                            form = CodeForm()
                            content = {
                                'form': form,
                                'message': 'Código no es de algún pago'
                            }
                            return render(request, 'sorteo/index.html', content)             
                else:
                    form = CodeForm()
                    content = {
                        'form': form,
                        'message': 'Código no es del mes actual'
                    }
                    return render(request, 'sorteo/index.html', content)
            else:
                form = CodeForm()
                content = {
                    'form': form,
                    'message': 'Código incorrecto'
                }
                return render(request, 'sorteo/index.html', content)
    else:
        form = CodeForm()
        content = {
            'form': form
        }
        return render(request, 'sorteo/index.html', content)

def running(request):
    if User.objects.filter(username=request.user).exists():  
        usuario = User.objects.get(username=request.user)    
        content = {
            'usuario': usuario,            
        }
    else:         
        content = {
            'usuario': 'anonymous',            
        }
    return render(request, 'sorteo/running.html', content)
