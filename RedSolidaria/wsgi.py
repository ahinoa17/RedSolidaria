"""
Configuración WSGI para el proyecto RedSolidaria.

Expone el objeto llamable WSGI como una variable a nivel de módulo llamada 'application'.

Para más información sobre este archivo, consulta:
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

# Módulo estándar de Python para interactuar con el sistema operativo
import os

# Importa la función para obtener la aplicación WSGI de Django
from django.core.wsgi import get_wsgi_application

# Establece la variable de entorno DJANGO_SETTINGS_MODULE para que Django
# sepa qué configuración usar (en este caso, RedSolidaria.settings)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'RedSolidaria.settings')

# Crea una instancia de la aplicación WSGI que será utilizada por el servidor WSGI
# Esta es la variable que los servidores WSGI buscarán para iniciar la aplicación
application = get_wsgi_application()
