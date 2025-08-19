# Importa la clase base AppConfig de Django necesaria para la configuración de la aplicación
from django.apps import AppConfig

# Configuración de la aplicación 'permutaciones'
class PermutacionesConfig(AppConfig):
    # Define el tipo de campo automático por defecto para los modelos
    default_auto_field = 'django.db.models.BigAutoField'
    
    # Nombre completo de la aplicación (debe coincidir con el nombre del paquete)
    name = 'permutaciones'