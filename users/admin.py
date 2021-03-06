from django.contrib import admin
from .models import Profile, Notificacion


class NotificacionAdminConfig(admin.ModelAdmin):
    model = Notificacion
    search_fields = ['usuario__username']
    list_filter = ('tipo', 'fecha', 'vista', 'sync')
    ordering = ('-fecha',)
    list_display = ('usuario', 'tipo', 'vista', 'sync', 'fecha')
    fieldsets = (
        (None, {'fields': ('usuario', 'tipo', 'vista', 'sync', 'fecha', 'contenido')}),
    )

class ProfileAdminConfig(admin.ModelAdmin):
    model = Profile
    search_fields = ['usuario__username']
    list_filter = ('sync',)
    ordering = ('-coins',)
    list_display = ('usuario', 'id', 'coins', 'sync')
    fieldsets = (
        (None, {'fields': ('usuario', 'coins', 'sync', 'imagen')}),
    )   
    """ add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('user_name', 'email', 'first_name', 'password1', 'password2', 'is_active', 'is_staff')}
         ), """

admin.site.register(Notificacion, NotificacionAdminConfig)

admin.site.register(Profile, ProfileAdminConfig)
