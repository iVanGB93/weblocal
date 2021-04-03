from django.contrib import admin
from django.forms import TextInput, Textarea, CharField
from django import forms
from .models import Oper, Recarga, EstadoServicio


class EstadosServiciosAdminConfig(admin.ModelAdmin):
    model = EstadoServicio
    search_fields = ['usuario__username']
    list_filter = ('internet', 'emby', 'jc', 'ftp')
    ordering = ('usuario',)
    list_display = ('usuario', 'internet', 'emby', 'jc', 'ftp')
    fieldsets = (
        (None, {'fields': ('usuario', )}),
        ('Internet', {'fields': ('internet', 'int_auto', 'int_time', 'int_tipo', 'int_horas')}),
        ('Emby', {'fields': ('emby', 'emby_auto', 'emby_time', 'emby_id')}),  
        ('FileZilla', {'fields': ('ftp', 'ftp_auto', 'ftp_time')}),
        ('Joven Club', {'fields': ('jc', 'jc_auto', 'jc_time')}),      
    )

class OpersAdminConfig(admin.ModelAdmin):
    model = Oper
    search_fields = ['usuario__username', 'code', 'tipo']
    list_filter = ('tipo', 'fecha', 'servicio')
    ordering = ('-fecha',)
    list_display = ('usuario', 'tipo', 'servicio', 'cantidad', 'fecha')
    fieldsets = (
        ('ID', {'fields': ('code', 'tipo')}),
        ('Datos', {'fields': ('usuario', 'servicio', 'cantidad', 'codRec', 'haciaDesde', 'fecha')}),
    )

class RecargasAdminConfig(admin.ModelAdmin):
    model = Recarga
    search_fields = ['usuario__username', 'code']
    list_filter = ('cantidad', 'fechaHecha')
    ordering = ('-fechaHecha',)
    list_display = ('code', 'usuario', 'cantidad', 'activa', 'fechaHecha', 'fechaUso')
    fieldsets = (
        (None, {'fields': ('code', 'usuario', 'cantidad', 'activa', 'fechaHecha', 'fechaUso')}),        
    )


admin.site.register(EstadoServicio, EstadosServiciosAdminConfig)

admin.site.register(Oper, OpersAdminConfig)

admin.site.register(Recarga, RecargasAdminConfig)