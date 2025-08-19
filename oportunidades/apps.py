# Importa la clase base AppConfig de Django
from django.apps import AppConfig

# Configuración de la aplicación 'oportunidades'
class OportunidadesConfig(AppConfig):
    # Define el campo autoincremental por defecto para los modelos
    default_auto_field = 'django.db.models.BigAutoField'
    
    # Nombre completo de Python de la aplicación
    name = 'oportunidades'