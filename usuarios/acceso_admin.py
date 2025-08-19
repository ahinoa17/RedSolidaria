# Importación de utilidades de redirección de Django
from django.shortcuts import redirect
# Importación de utilidades para manejo de URLs
from django.urls import reverse
# Importación de la configuración del proyecto
from django.conf import settings
# Importación del sistema de mensajes de Django
from django.contrib import messages


class ControlAccesoAdmin:
    """
    Controla el acceso al panel de administración.
    Solo permite acceso a superusuarios o usuarios con acceso_admin=True.
    """
    def __init__(self, get_response):
        # Almacena la función get_response que se llamará después del procesamiento
        self.get_response = get_response
        # Rutas que no requieren verificación de permisos
        self.admin_paths = [
            '/admin/login/',
            '/admin/logout/',
            '/admin/password_reset/',
            '/admin/jsi18n/',
            '/admin/static/',
            '/admin/media/'
        ]


    def __call__(self, request):
        # Verificar si la ruta comienza con /admin/
        if request.path.startswith('/admin/'):
            # Comprobar si la ruta actual no está en las rutas permitidas
            if not any(request.path.startswith(path) for path in self.admin_paths):
                # Verificar si el usuario está autenticado
                if hasattr(request, 'user') and request.user.is_authenticated:
                    # Verificar si el usuario es superusuario o tiene acceso de administrador
                    if not (request.user.is_superuser or getattr(request.user, 'acceso_admin', False)):
                        # Redirigir a la página de inicio si no tiene permisos
                        return redirect('home')
                else:
                    # Si el usuario no está autenticado, redirigir al login
                    from django.contrib.auth.views import redirect_to_login
                    return redirect_to_login(request.path)
        
        # Continuar con el procesamiento normal de la solicitud
        response = self.get_response(request)
        return response
