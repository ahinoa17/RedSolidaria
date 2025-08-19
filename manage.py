#!/usr/bin/env python
"""
Utilidad de línea de comandos de Django para tareas administrativas.
Este archivo es el punto de entrada para los comandos de gestión de Django.
"""

# Importaciones estándar de Python
import os  # Para interactuar con el sistema operativo
import sys  # Para acceder a los argumentos de la línea de comandos


def main():
    """
    Función principal que ejecuta tareas administrativas de Django.
    Configura el entorno y ejecuta el comando solicitado.
    """
    # Establece la variable de entorno DJANGO_SETTINGS_MODULE que indica
    # a Django qué configuración usar (en este caso, RedSolidaria.settings)
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'RedSolidaria.settings')
    
    try:
        # Intenta importar la función execute_from_command_line de Django
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        # Maneja el error si Django no está instalado o no está disponible
        raise ImportError(
            "No se pudo importar Django. ¿Está instalado y "
            "disponible en su variable de entorno PYTHONPATH? ¿Olvidó "
            "activar un entorno virtual?"
        ) from exc
    
    # Ejecuta el comando de gestión de Django con los argumentos proporcionados
    # sys.argv contiene los argumentos de la línea de comandos
    execute_from_command_line(sys.argv)


# Punto de entrada principal del script
if __name__ == '__main__':
    # Llama a la función main cuando se ejecuta este script directamente
    main()
