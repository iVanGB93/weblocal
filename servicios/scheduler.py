from apscheduler.schedulers.background import BackgroundScheduler
from django.utils import timezone
from .models import EstadoServicio, Oper
from users.models import Profile
from django.contrib.auth.models import User
from decouple import config
from datetime import timedelta
import requests
import xml.etree.ElementTree
import subprocess
import routeros_api
import os
from django.core.mail.message import EmailMessage

from sync.actions import EmailSending

emailAlerts = config('EMAIL_ALERTS', cast=lambda x: x.split(','))

def crearOper(usuario, servicio, cantidad):
    userinst = User.objects.get(username=usuario)           
    nuevaOper = Oper(tipo='PAGO', usuario=userinst, servicio=servicio, cantidad=cantidad)
    nuevaOper.save()
    code = nuevaOper.code
    return code

def conectar_mikrotik(ip, username, password, usuario, servicio):
    result = {'estado': False}
    try:
        connection = routeros_api.RouterOsApiPool(ip, username=username, password=password, plaintext_login=True)
        api = connection.get_api()
    except:
        result['mensaje'] = 'Falló la conexión con el mikrotik, intente más tarde.'
        return result
    if servicio == 'internet':
        lista_usuarios = api.get_resource('/ip/hotspot/user')
        usuario = lista_usuarios.get(name=usuario)
    else:
        lista_usuarios = api.get_resource('/ip/firewall/address-list')
        usuario = lista_usuarios.get(comment=usuario)     
    if usuario != []:        
        lista_usuarios.set(id=usuario[0]['id'], disabled='true')
        result['estado'] = True
        return result
    else:
        result['mensaje'] = "No estaba el usuario"
        return result

#FILEZILLA
user_xml_fmt = '''
        <User Name="{username}">
            <Option Name="Pass">{md5_pwd}</Option>
            <Option Name="Group">{group}</Option>
            <Option Name="Bypass server userlimit">2</Option>
            <Option Name="User Limit">0</Option>
            <Option Name="IP Limit">0</Option>
            <Option Name="Enabled">2</Option>
            <Option Name="Comments" />
            <Option Name="ForceSsl">2</Option>
            <IpFilter>
                <Disallowed />
                <Allowed />
            </IpFilter>
            <Permissions />
            <SpeedLimits DlType="0" DlLimit="10" ServerDlLimitBypass="2" UlType="0" UlLimit="10" ServerUlLimitBypass="2">
                <Download />
                <Upload />
            </SpeedLimits>
        </User>
'''

folder = 'C:/Program Files (x86)/FileZilla Server'
xml_path = os.path.join(folder, 'FileZilla Server.xml')
exe_path = os.path.join(folder, 'FileZilla Server.exe')

class DDDManager():

    def __init__(self, filename):
        self.filename = filename

    def setup(self):
        self.tree = xml.etree.ElementTree.parse(self.filename)
        self.root = self.tree.getroot()
        self.user_tree = self.root.findall('Users')[0]
        return self

    def remove_user(self, username):
        for user in self.user_tree:
            if user.get('Name') == username:
                self.user_tree.remove(user)

    def dump(self):
        self.tree.write(self.filename)

def quitarFTP(username):

    manager = DDDManager(xml_path).setup()   
   
    manager.remove_user(username)

    manager.dump()
    subprocess.run([exe_path, '/reload-config'], shell=True)
#Fin FileZilla

def chequeoInternet():    
    inter = EstadoServicio.objects.filter(internet=True)
    for i in inter:   
        exp = i.int_time
        if exp:
            if exp <= timezone.now():
                usuario = User.objects.get(username=i.usuario)
                profile = Profile.objects.get(usuario=usuario.id)
                if i.int_auto and i.int_duracion != None and i.int_velocidad != None:                 
                    if i.int_tipo == "internet-24h":
                        costo_base = int(config('INTERNET_PRICE_SEMANAL'))
                        if i.int_duracion == 'semanal':            
                            dias = 7
                            if i.int_velocidad == '1mb':
                                costo = costo_base
                            elif i.int_velocidad == '2mb':
                                costo = costo_base * 2
                            elif i.int_velocidad == '3mb':
                                costo = costo_base * 3
                            elif i.int_velocidad == '4mb':
                                costo = costo_base * 4
                        if i.int_duracion == 'mensual':            
                            dias = 30
                            if i.int_velocidad == '1mb':
                                costo = costo_base * 4
                            elif i.int_velocidad == '2mb':
                                costo = costo_base * 2 * 4
                            elif i.int_velocidad == '3mb':
                                costo = costo_base * 3 * 4
                            elif i.int_velocidad == '4mb':
                                costo = costo_base * 4 * 4
                        if profile.coins < costo:
                            resultado = conectar_mikrotik(config('MK1_IP'), config('MK1_USER'), config('MK1_PASSWORD'), usuario.username, 'internet')                   
                            if resultado['estado']:
                                i.internet = False
                                i.int_time = None
                                i.sync = False
                                i.save()
                                email = EmailMessage('QbaRed - Rechazo de pago', f'No se pudo reanudar su servicio { i.int_tipo }, no tiene suficientes coins, por favor recargue. Saludos QbaRed.', None, [usuario.email])
                                EmailSending(email).start()
                            else:
                                mensaje = resultado['mensaje']
                                email = EmailMessage('Error al quitar servicio', f'No se pudo quitar el servicio { i.int_tipo } del usuario { usuario.username }, MENSAJE: { mensaje }', None, emailAlerts)
                                EmailSending(email).start()
                        else:
                            profile.coins = profile.coins - costo
                            i.int_time = timezone.now() + timedelta(days=dias)
                            profile.sync = False
                            profile.save()
                            i.sync = False
                            i.save()
                            code = crearOper(usuario.username, "internet-24h", costo)
                            email = EmailMessage('QbaRed - Pago confirmado', f'Se ha reanudado su servicio { i.int_tipo }, esperamos que disfrute su tiempo y que no tenga mucho tufe la red ;-) Utilice este código para el sorteo mensual: "{ code }". Saludos QbaRed.', None, [usuario.email])
                            EmailSending(email).start()
                else:                    
                    resultado = conectar_mikrotik(config('MK1_IP'), config('MK1_USER'), config('MK1_PASSWORD'), usuario.username, 'internet')                   
                    if resultado['estado']:
                        i.internet = False
                        i.int_time = None
                        i.sync = False
                        i.save()
                        email = EmailMessage('QbaRed - Tiempo agotado', f'Se termino el tiempo del { i.int_tipo }, para volver a usarlo vaya a nuestro portal del usuario. Saludos QbaRed.', None, [usuario.email])    
                        EmailSending(email).start()
                    else:
                        mensaje = resultado['mensaje']
                        email = EmailMessage('Error al quitar servicio', f'No se pudo quitar el servicio { i.int_tipo } del usuario { usuario.username }, MENSAJE: { mensaje }', None, [usuario.email])
                        EmailSending(email).start()

def chequeo():    
    emb = EstadoServicio.objects.filter(emby=True)
    jclub = EstadoServicio.objects.filter(jc=True)
    filezilla = EstadoServicio.objects.filter(ftp=True)    
    for e in emb:
        exp = e.emby_time
        if exp:
            if exp <= timezone.now():
                usuario = User.objects.get(username=e.usuario)
                profile = Profile.objects.get(usuario=usuario.id)
                emby_ip = config('EMBY_IP')            
                emby_api_key = config('EMBY_API_KEY')
                embyPrice = int(config('EMBY_PRICE'))         
                url = f'{ emby_ip }/Users/{ e.emby_id }?api_key={ emby_api_key }' 
                if e.emby_auto:                    
                    if profile.coins >= embyPrice:
                        profile.coins = profile.coins - embyPrice
                        profile.sync = False
                        profile.save()
                        e.emby_time = timezone.now() + timedelta(days=30)
                        e.sync = False
                        e.save()
                        code = crearOper(usuario.username, "Emby", embyPrice)
                        email = EmailMessage('QbaRed - Pago confirmado', f'Se ha reanudado su servicio emby, esperamos que disfrute su tiempo y que no tenga mucho tufe la red ;-) Utilice este código para el sorteo mensual: "{ code }". Saludos QbaRed.', None, [usuario.email])
                        EmailSending(email).start()
                    else:
                        email = EmailMessage('QbaRed - Rechazo de pago', 'No se pudo reanudar su servicio emby, no tiene suficientes coins, por favor recargue. Saludos QbaRed.', None, [usuario.email])                       
                        EmailSending(email).start()
                        connect = requests.delete(url=url)
                        if connect.status_code == 204:
                            e.emby = False
                            e.emby_time = None
                            e.sync = False
                            e.save()
                        else:           
                            email = EmailMessage(f'Quitar Emby a { usuario.username }', f'Tiempo acabado y no se desactiva su cuenta.', None, emailAlerts)
                            EmailSending(email).start()
                else:
                    email = EmailMessage('QbaRed - Tiempo agotado', 'Se terminó el tiempo de su servicio emby, para volver a usarlo vaya a nuestro portal del usuario. Saludos QbaRed.', None, [usuario.email])
                    EmailSending(email).start()
                    connect = requests.delete(url=url)
                    if connect.status_code == 204:
                        e.emby = False
                        e.emby_time = None
                        e.sync = False
                        e.save()
                    else:                                 
                        email = EmailMessage(f'Quitar Emby a { usuario.username }', f'Tiempo acabado y no se desactiva su cuenta.', None, emailAlerts)
                        EmailSending(email).start()
    for j in jclub:   
        exp = j.jc_time
        if exp:
            if exp <= timezone.now():
                usuario = User.objects.get(username=j.usuario)
                profile = Profile.objects.get(usuario=usuario.id)
                if j.jc_auto:                    
                    if profile.coins >= 100:
                        profile.coins = profile.coins - 100
                        profile.sync = False
                        profile.save()
                        j.jc_time = timezone.now() + timedelta(days=30)
                        j.sync = False
                        j.save()
                        code = crearOper(usuario.username, "Joven Club", 100)
                        email = EmailMessage('QbaRed - Pago confirmado', f'Se ha reanudado su servicio JovenClub, esperamos que disfrute su tiempo y que no tenga mucho tufe la red ;-) Utilice este código para el sorteo mensual: "{ code }". Saludos QbaRed.', None, [usuario.email])
                        EmailSending(email).start()
                    else:
                        resultado = conectar_mikrotik(config('MK2_IP'), config('MK2_USER'), config('MK2_PASSWORD'), usuario.username, 'joven-club')
                        if resultado['estado']:
                            j.jc = False
                            j.jc_time = None
                            j.sync = False
                            j.save()
                            email = EmailMessage('QbaRed - Rechazo de pago', 'No se pudo reanudar su servicio JovenClub, no tiene suficientes coins, por favor recargue. Saludos QbaRed.', None, [usuario.email])
                            EmailSending(email).start()
                        else:
                            mensaje = resultado['mensaje']
                            email = EmailMessage('Error al quitar servicio', f'No se pudo quitar el servicio Joven Club, MENSAJE: { mensaje }', None, emailAlerts)
                            EmailSending(email).start()
                else:
                    resultado = conectar_mikrotik(config('MK2_IP'), config('MK2_USER'), config('MK2_PASSWORD'), usuario.username, 'joven-club')
                    if resultado['estado']:
                        j.jc = False
                        j.jc_time = None
                        j.sync = False
                        j.save()
                        email = EmailMessage('QbaRed - Tiempo agotado', 'Se termino el tiempo de su servicio Joven Club, para volver a usarlo vaya a nuestro portal del usuario. Saludos QbaRed.', None, [usuario.email])
                        EmailSending(email).start()
    for f in filezilla:   
        exp = f.ftp_time       
        if exp:
            if exp <= timezone.now():
                usuario = User.objects.get(username=f.usuario)
                profile = Profile.objects.get(usuario=usuario.id)
                ftpPrice = int(config('FTP_PRICE'))          
                if f.ftp_auto:
                    if profile.coins >= ftpPrice:
                        profile.coins = profile.coins - ftpPrice
                        profile.sync = False
                        profile.save()
                        f.ftp_time = timezone.now() + timedelta(days=30)
                        f.sync = False
                        f.save()
                        code = crearOper(usuario.username, "FileZilla", ftpPrice)
                        email = EmailMessage('QbaRed - Pago confirmado', f'Se ha reanudado su servicio FileZilla, esperamos que disfrute su tiempo y que no tenga mucho tufe la red ;-) Utilice este código para el sorteo mensual: "{ code }". Saludos QbaRed.', 'RedCentroHabanaCuba@gmail.com', [usuario.email])
                        EmailSending(email).start()
                    else:
                        quitarFTP(usuario.username)                          
                        f.ftp = False
                        f.ftp_time = None
                        f.sync = False
                        f.save() 
                        email = EmailMessage('QbaRed - Rechazo de pago', 'No se pudo reanudar su servicio FileZilla, no tiene suficientes coins, por favor recargue. Saludos QbaRed.', 'RedCentroHabanaCuba@gmail.com', [usuario.email])
                        EmailSending(email).start()
                else:
                    quitarFTP(usuario.username)                          
                    f.ftp = False
                    f.ftp_time = None
                    f.sync = False
                    f.save()          

def tiempoAcabado():
    scheduler = BackgroundScheduler()
    scheduler.add_job(chequeoInternet, 'interval', minutes=5)
    scheduler.add_job(chequeo, 'interval', minutes=30)
    scheduler.start()