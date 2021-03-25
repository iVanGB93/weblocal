from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('web.urls')),
    path('sorteo/', include('sorteo.urls')),
    path('portal/', include('portal.urls')),
    path('api/servicios/', include('servicios.api.urls')),
    path('api/users/', include('users.api.urls')),
    path('portal/password-reset/confirm/<uidb64>/<token>/',
        TemplateView.as_view(template_name="portal/index.html"), name='password_reset_confirm'),
]
