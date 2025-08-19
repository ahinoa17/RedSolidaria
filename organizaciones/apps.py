# Importa la clase base AppConfig de Django
from django.apps import AppConfig

# Define la configuración de la aplicación 'organizaciones'
class OrganizacionesConfig(AppConfig):
    # Especifica el tipo de campo automático por defecto para los modelos
    # BigAutoField es un entero de 64 bits, similar a AutoField pero garantiza
    # que no se agotarán los IDs (hasta 9,223,372,036,854,775,807 registros)
    default_auto_field = 'django.db.models.BigAutoField'
    
    # Nombre completo de Python de la aplicación (debe coincidir con el nombre del paquete)
    name = 'organizaciones'