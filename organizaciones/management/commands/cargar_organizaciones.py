from django.core.management.base import BaseCommand
from organizaciones.models import Organizacion
from django.utils.text import slugify
import os
from django.conf import settings

class Command(BaseCommand):
    help = 'Carga las organizaciones iniciales en la base de datos'

    def handle(self, *args, **options):
        # Lista de organizaciones a cargar
        organizaciones = [
            {
                'nombre': 'Fundación Manos Solidarias',
                'descripcion': 'Organización dedicada a ayudar a comunidades vulnerables a través de programas de desarrollo social.',
                'contacto_email': 'contacto@manossolidarias.org',
                'telefono': '+1234567890',
                'direccion': 'Calle Principal #123, Ciudad',
                'logo': 'organizaciones/logos/fundacion-manos-solidarias.png',
                'activa': True
            },
            {
                'nombre': 'Fundación Natura Bolivia',
                'descripcion': 'Trabajando por la conservación de la biodiversidad y el desarrollo sostenible en Bolivia.',
                'contacto_email': 'info@naturabolivia.org',
                'telefono': '+59112345678',
                'direccion': 'Av. Ecológica #456, Santa Cruz',
                'logo': 'organizaciones/logos/fundacion-natura-bolivia.jpeg',
                'activa': True
            },
            {
                'nombre': 'Fundación Teletón',
                'descripcion': 'Ayudando a niños y jóvenes con discapacidad a través de rehabilitación integral.',
                'contacto_email': 'contacto@teleton.org',
                'telefono': '+1234567890',
                'direccion': 'Av. Siempre Viva #789',
                'logo': 'organizaciones/logos/fundacion-teleton.png',
                'activa': True
            },
            {
                'nombre': 'Cruz Roja Mexicana',
                'descripcion': 'Brindando ayuda humanitaria y servicios de salud a las comunidades más necesitadas.',
                'contacto_email': 'info@cruzrojamexicana.org',
                'telefono': '+525512345678',
                'direccion': 'Av. Ejército Nacional #1032, Ciudad de México',
                'logo': 'organizaciones/logos/cruz-roja-mexicana.jpg',
                'activa': True
            },
            {
                'nombre': 'Fundación Pies Descalzos',
                'descripcion': 'Trabajando por la educación de calidad para niños y niñas en situación de vulnerabilidad.',
                'contacto_email': 'info@fundacionpiesdescalzos.com',
                'telefono': '+5712345678',
                'direccion': 'Carrera 7 #75-01, Bogotá',
                'logo': 'organizaciones/logos/fundacion-pies-descalzos.jpg',
                'activa': True
            },
            {
                'nombre': 'Fundación Pro Vivienda Social',
                'descripcion': 'Promoviendo el acceso a vivienda digna para familias de bajos recursos.',
                'contacto_email': 'contacto@provivienda.org',
                'telefono': '+541112345678',
                'direccion': 'Av. Corrientes 1234, Buenos Aires',
                'logo': 'organizaciones/logos/fundacion-pro-vivienda-social.jpg',
                'activa': True
            },
            {
                'nombre': 'Aldeas Infantiles SOS',
                'descripcion': 'Protegiendo a niños, niñas y adolescentes que han perdido el cuidado familiar.',
                'contacto_email': 'info@aldeasinfantiles.org',
                'telefono': '+541123456789',
                'direccion': 'Av. Santa Fe 4209, Buenos Aires',
                'logo': 'organizaciones/logos/aldeas-infantiles-sos.webp',
                'activa': True
            },
            {
                'nombre': 'Fundación Amigos del Río San Juan',
                'descripcion': 'Trabajando por la conservación y desarrollo sostenible de la cuenca del Río San Juan.',
                'contacto_email': 'info@amigosdelsanjuan.org',
                'telefono': '+50521234567',
                'direccion': 'Costado Sur Parque Central, San Carlos',
                'logo': 'organizaciones/logos/fundacion-amigos-rio-san-juan.jpeg',
                'activa': True
            },
            {
                'nombre': 'Fundación Vida Silvestre Argentina',
                'descripcion': 'Protegiendo la naturaleza, promoviendo el uso sustentable de los recursos naturales.',
                'contacto_email': 'info@vidasilvestre.org.ar',
                'telefono': '+541143313633',
                'direccion': 'Defensa 251, Buenos Aires',
                'logo': 'organizaciones/logos/fundacion-vida-silvestre-argentina.jpg',
                'activa': True
            },
            {
                'nombre': 'Fundación Paraguaya',
                'descripcion': 'Desarrollando soluciones innovadoras para la eliminación de la pobreza y el desempleo.',
                'contacto_email': 'info@fundacionparaguaya.org.py',
                'telefono': '+59521296081',
                'direccion': 'Av. Molas López 369, Asunción',
                'logo': 'organizaciones/logos/fundacion-paraguaya.jpg',
                'activa': True
            }
        ]

        # Contadores para el resumen
        creadas = 0
        actualizadas = 0

        for org_data in organizaciones:
            # Generar el slug a partir del nombre
            org_data['slug'] = slugify(org_data['nombre'])
            
            # Verificar si ya existe una organización con el mismo nombre o slug
            org, created = Organizacion.objects.update_or_create(
                nombre=org_data['nombre'],
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
            
            if created:
                creadas += 1
                self.stdout.write(self.style.SUCCESS(f'Creada: {org.nombre}'))
            else:
                actualizadas += 1
                self.stdout.write(self.style.WARNING(f'Actualizada: {org.nombre}'))
        
        self.stdout.write(self.style.SUCCESS(f'\nProceso completado.\nOrganizaciones creadas: {creadas}\nOrganizaciones actualizadas: {actualizadas}'))
