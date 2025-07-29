from django.contrib import admin
from django.urls import path, include
from usuarios import views as usuarios_views

urlpatterns = [
    path('', usuarios_views.home, name='home'),
    path('admin/', admin.site.urls),
    path('oportunidades/', include('oportunidades.urls')),
    path('usuarios/', include('usuarios.urls')),
    path('organizaciones/', include('organizaciones.urls')),
    path('inscripciones/', include('inscripciones.urls')),
    path('reportes/', include('reportes.urls')),
    path('permutaciones/', include('permutaciones.urls')),
    path('accounts/', include('django.contrib.auth.urls')),  # <--- AGREGA ESTA LÍNEA
]