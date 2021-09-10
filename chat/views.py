# chat/views.py
from django.shortcuts import redirect, render
from django.contrib.auth.models import User

from .models import Chat

def index(request):
    content = {'usuarios': User.objects.all()}
    return render(request, 'chat/index.html', content)

def room(request, id_usuario=None):
    if id_usuario == None:
        content = {'usuarios': User.objects.all()}
        return render(request, 'chat/room.html', content)
    if User.objects.filter(id=id_usuario).exists():
        usuario2 = User.objects.get(id=id_usuario)
        chats = request.user.chat_set.all()
        existe = False
        for chat in chats:
            if usuario2 in chat.participantes.all():
                chat = chat
                existe = True
                break
        if not existe:
            chat = Chat()
            chat.save()
            chat.participantes.add(request.user, usuario2)
        chat_id = chat.id
        img_url = usuario2.profile.imagen.url
        if not request.user in chat.participantes.all():
            return redirect('chat:index')
        return render(request, 'chat/room.html', {
            'chat_id': chat_id,
            'img_url': img_url,
            'usuarios': User.objects.all()
        })
    else:
        return redirect('chat:index')