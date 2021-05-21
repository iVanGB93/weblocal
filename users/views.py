from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .forms import LoginForm, RegisterForm
from sync.syncs import actualizacion_usuario


def entrar(request):
    if request.user.is_authenticated:
        return redirect ('/')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if User.objects.filter(username=username).exists():            
            form = LoginForm(request.POST)
            if form.is_valid():
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('web:index')
                else:
                    form = LoginForm()
                    error = "Contraseña Incorrecta"
                    content = {'error': error, 'form': form}
                    return render(request, 'users/login.html', content)
        else:            
            form = LoginForm()
            error = "Usuario NO Existe"
            content = {'error': error, 'form': form}
            return render(request, 'users/login.html', content)
    else:
        form = LoginForm()
        content = {'form': form}
        return render(request, 'users/login.html', content)

def register(request):
    if request.user.is_authenticated:
        return redirect ('/')
    if request.method == 'POST':
        username = request.POST['username']
        if User.objects.filter(username=username).exists():
            form = RegisterForm()
            error = "Nombre de usuario en uso."
            content = {'error': error, 'form': form}
            return render(request, 'users/register.html', content)
        #if actualizacion_usuario('check', username):
        #    form = RegisterForm()
        #    error = "Nombre de usuario en uso."
        #    content = {'error': error, 'form': form}
        #    return render(request, 'users/register.html', content)
        else:
            email = request.POST['email']
            if User.objects.filter(email=email).exists():
                form = RegisterForm()
                error = "Correo en uso."
                content = {'error': error, 'form': form}
                return render(request, 'users/register.html', content)
            else:
                email2 = request.POST['email2']
                if email != email2:
                    form = RegisterForm()
                    error = "Los correos no coinciden."
                    content = {'error': error, 'form': form}
                    return render(request, 'users/register.html', content)
                else:
                    form = RegisterForm(request.POST)
                    if form.is_valid():
                        user = form.save(commit=False)
                        password = request.POST['password']
                        user.set_password(password)
                        user.save()
                        new_user = authenticate(username=user.username, password=password)  
                        if actualizacion_usuario('nuevo', user.username, user.email, password):
                            login(request, new_user)
                            return redirect('web:index')
                        else:
                            form = RegisterForm()
                            error = "Error de comunicación."
                            content = {'error': error, 'form': form}
                            return render(request, 'users/register.html', content)
                    else:
                        form = RegisterForm()
                        error = "Error de campo."
                        content = {'error': error, 'form': form}
                        return render(request, 'users/register.html', content)                                      
    else:
        form = RegisterForm()
        content = {'form': form}
        return render(request, 'users/register.html', content)
    
def salir(request):
    logout(request)
    return redirect('/')