# Importa la clase base AppConfig de Django necesaria para la configuración de aplicaciones
from django.apps import AppConfig


class UsuariosConfig(AppConfig):
    """
    Configuración de la aplicación 'usuarios'.
    
    Esta clase define la configuración específica para la aplicación de usuarios
    en el proyecto. Hereda de AppConfig que es la clase base para todas las
    configuraciones de aplicaciones en Django.
    """
    
    # Define el tipo de campo automático por defecto para las claves primarias
    # Se utiliza BigAutoField que es un entero de 64 bits, adecuado para tablas grandes
    default_auto_field = 'django.db.models.BigAutoField'
    
    # Nombre completo de Python de la aplicación (debe coincidir con el nombre del paquete)
    # Django usa este nombre para buscar la aplicación en INSTALLED_APPS
    name = 'usuarios'
