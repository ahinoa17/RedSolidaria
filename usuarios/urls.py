# Importa la función path para definir patrones de URL
from django.urls import path
# Importa las vistas definidas en el archivo views.py del mismo directorio
from . import views


# Lista de patrones URL para la aplicación de usuarios
urlpatterns = [
    # Página de inicio de la aplicación de usuarios
    # URL: /usuarios/
    path('', views.home, name='home'),  # Página de inicio
    
    # Formulario de registro para nuevos voluntarios
    # URL: /usuarios/registro/voluntario/
    path('registro/voluntario/', 
         views.registro_voluntario, 
         name='registro_voluntario'),
    
    # Página de inicio de sesión para usuarios existentes
    # URL: /usuarios/login/
    path('login/', 
         views.login_view, 
         name='login'),
    
    # Cierre de sesión del usuario actual
    # URL: /usuarios/logout/
    path('logout/', 
         views.logout_view, 
         name='logout'),
    
    # Gestión de usuarios (solo superusuarios)
    path('gestion/usuarios/', 
         views.listar_usuarios, 
         name='listar_usuarios'),
    
    path('gestion/usuarios/editar/<int:usuario_id>/', 
         views.editar_usuario, 
         name='editar_usuario'),
    
    path('gestion/usuarios/toggle-estado/<int:usuario_id>/', 
         views.toggle_estado_usuario, 
         name='toggle_estado_usuario'),
]