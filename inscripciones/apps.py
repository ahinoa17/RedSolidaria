# Importación de la configuración de aplicaciones de Django
from django.apps import AppConfig


class InscripcionesConfig(AppConfig):
    """
    Configuración de la aplicación 'inscripciones' para el proyecto RedSolidaria.
    
    Esta clase define la configuración específica de la aplicación de inscripciones,
    incluyendo el tipo de campo automático predeterminado y el nombre de la aplicación.
    """
    
    # Define el tipo de campo automático que se usará para los modelos
    default_auto_field = 'django.db.models.BigAutoField'
    
    # Nombre completo de Python de la aplicación
    name = 'inscripciones'