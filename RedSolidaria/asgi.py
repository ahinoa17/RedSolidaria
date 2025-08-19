"""
Configuración ASGI para el proyecto RedSolidaria.

Expone el objeto llamable ASGI como una variable a nivel de módulo llamada 'application'.

Para más información sobre este archivo, consulta:
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

# Módulo estándar de Python para interactuar con el sistema operativo
import os

# Importa la función para obtener la aplicación ASGI de Django
from django.core.asgi import get_asgi_application

# Establece la variable de entorno DJANGO_SETTINGS_MODULE para que Django
# sepa qué configuración usar (en este caso, RedSolidaria.settings)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'RedSolidaria.settings')

# Crea una instancia de la aplicación ASGI que será utilizada por el servidor ASGI
# Esta es la variable que los servidores ASGI buscarán para iniciar la aplicación
application = get_asgi_application()
