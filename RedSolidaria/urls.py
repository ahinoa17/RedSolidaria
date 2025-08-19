# Importaciones del núcleo de Django
from django.contrib import admin  # Interfaz de administración
from django.urls import path, include  # Funciones para definir URLs
from django.views.generic import RedirectView  # Vistas genéricas para redirecciones
from django.contrib.auth import views as auth_views  # Vistas de autenticación
from django.conf import settings  # Configuración del proyecto
from django.conf.urls.static import static  # Para servir archivos estáticos en desarrollo

# Definición de patrones URL principales del proyecto
urlpatterns = [
    # Panel de administración de Django
    path('admin/', admin.site.urls),
    
    # Incluye las URLs de la aplicación de usuarios
    path('usuarios/', include('usuarios.urls')),
    
    # Ruta raíz: redirige a la página de inicio de sesión
    path('', auth_views.LoginView.as_view(
        template_name='registration/login.html'
    ), name='login'),
    
    # Inclusión de URLs de las demás aplicaciones del proyecto
    path('oportunidades/', include('oportunidades.urls')),  # Gestión de oportunidades
    path('organizaciones/', include('organizaciones.urls')),  # Gestión de organizaciones
    path('inscripciones/', include('inscripciones.urls')),  # Sistema de inscripciones
    path('permutaciones/', include('permutaciones.urls', namespace='permutaciones')),  # Sistema de permutas
# Configuración para servir archivos multimedia en desarrollo
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)