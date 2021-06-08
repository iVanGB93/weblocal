from django.contrib import admin
from .models import Publicacion

class PublicacionAdminConfig(admin.ModelAdmin):
    model = Publicacion
    search_fields = ['autor__username', 'titulo']
    list_filter = ('tema', 'online')
    ordering = ('-fecha',)
    list_display = ('autor', 'tema', 'titulo', 'online', 'fecha')
    fieldsets = (
        ('ID', {'fields': ('usuario', 'online')}),
        ('Publicacion', {'fields': ('tema', 'titulo', 'contenido')}),
        ('Fecha', {'fields': ('mes', 'fecha')}),
        ('Imagenes', {'fields': ('imagen1', 'imagen2', 'imagen3')}),
    )

admin.site.register(Publicacion, PublicacionAdminConfig)
