from django.contrib.auth.models import User
from decouple import config

def nuevo_usuario(method):
    if method == 'check':
        print("CHECKING")
    elif method == 'nuevo':
        print("AGREGANDO")
    else:
        print("ALGO MAS")

def actualizacion_usuario():
    pass

def actualizacion_internet():
    pass

def actualizacion_jovenclub():
    pass

def actualizacion_emby():
    pass

def actualizacion_filezilla():
    pass
