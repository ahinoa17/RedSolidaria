# Importaciones necesarias para el comando personalizado
from django.core.management.base import BaseCommand
from organizaciones.models import Organizacion
from django.utils.text import slugify  # Para generar slugs a partir de texto
import os
from django.conf import settings

# Definición del comando personalizado
class Command(BaseCommand):
    help = 'Carga las organizaciones iniciales en la base de datos'

    def handle(self, *args, **options):
        # Lista de diccionarios con la información de cada organización
        # Cada diccionario contiene los campos del modelo Organizacion
        organizaciones = [
            {
                'nombre': 'Fundación Manos Solidarias',
                'descripcion': 'Organización dedicada a ayudar...',
                'contacto_email': 'contacto@manossolidarias.org',
                'telefono': '+1234567890',
                'direccion': 'Calle Principal #123, Ciudad',
                'logo': 'organizaciones/logos/fundacion-manos-solidarias.png',
                'activa': True
            },
            # ... más organizaciones ...
        ]

        # Contadores para llevar registro de las operaciones realizadas
        creadas = 0      # Cuenta organizaciones nuevas creadas
        actualizadas = 0  # Cuenta organizaciones existentes actualizadas

        # Procesa cada organización en la lista
        for org_data in organizaciones:
            # Genera un slug a partir del nombre para URLs amigables
            # Ejemplo: "Fundación Manos" -> "fundacion-manos"
            org_data['slug'] = slugify(org_data['nombre'])
            
            # Busca una organización existente o crea una nueva
            # update_or_create() devuelve una tupla (objeto, booleano_creado)
            org, created = Organizacion.objects.update_or_create(
                # Campo usado para buscar coincidencias
                nombre=org_data['nombre'],
                # Valores a actualizar o establecer
                defaults={
                    'descripcion': org_data['descripcion'],
                    'contacto_email': org_data['contacto_email'],
                    'telefono': org_data['telefono'],
                    'direccion': org_data['direccion'],
                    'logo': org_data['logo'],
                    'activa': org_data['activa'],
                    'slug': org_data['slug']
                }
            )
            
            # Muestra retroalimentación en la consola
            if created:
                creadas += 1
                # Muestra en verde las organizaciones nuevas
                self.stdout.write(self.style.SUCCESS(f'Creada: {org.nombre}'))
            else:
                actualizadas += 1
                # Muestra en amarillo las actualizaciones
                self.stdout.write(self.style.WARNING(f'Actualizada: {org.nombre}'))
        
        # Muestra un resumen al finalizar
        self.stdout.write(self.style.SUCCESS(
            f'\nProceso completado.\n'
            f'Organizaciones creadas: {creadas}\n'
            f'Organizaciones actualizadas: {actualizadas}'
        ))