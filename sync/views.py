from django.shortcuts import render
from .syncs import *

def nuevo_usuario(request):
    if request.method == 'POST':
        nuevo_usuario('nuevo', 'username', 'password', 'email')
    if request.method == 'PUT':
        pass
    if request.method == 'GET':
        nuevo_usuario('check', 'username', 'password', 'email')
    else:
        print("ALGO MAS")
