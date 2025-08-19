# Importa el módulo models de Django para definir modelos de base de datos
from django.db import models
# Importa slugify para crear URLs amigables
from django.utils.text import slugify


class Organizacion(models.Model):
    """
    Modelo que representa una organización en el sistema.
    Hereda de models.Model, la clase base para todos los modelos de Django.
    """
    
    # Campo de texto para el nombre de la organización (máx. 100 caracteres, único)
    nombre = models.CharField(max_length=100, unique=True)
    
    # Campo de texto largo para la descripción
    descripcion = models.TextField()
    
    # Campo para el correo electrónico de contacto (validado como email)
    contacto_email = models.EmailField()
    
    # Campo para el teléfono (opcional, máx. 20 caracteres)
    telefono = models.CharField(max_length=20, blank=True)
    
    # Campo para la dirección (opcional, máx. 255 caracteres)
    direccion = models.CharField(max_length=255, blank=True)
    
    # Campo para el nombre del archivo del logo (almacenado en static/img/logos/)
    logo = models.CharField(max_length=100, blank=True, 
                          help_text='Nombre del archivo del logo en static/img/logos/')
    
    # Campo booleano que indica si la organización está activa (por defecto: True)
    activa = models.BooleanField(default=True)
    
    # Campo de fecha/hora que se establece automáticamente al crear el registro
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    # Campo de fecha/hora que se actualiza automáticamente al guardar el registro
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        """
        Representación en string del objeto.
        Devuelve el nombre de la organización.
        """
        return self.nombre

    @property
    def logo_url(self):
        """
        Propiedad que devuelve la URL completa del logo.
        Si no hay logo definido, devuelve una imagen por defecto.
        """
        if self.logo:
            # Construye la ruta al logo si existe
            return f'/static/img/logos/{self.logo}'
        # Ruta a la imagen por defecto si no hay logo
        return '/static/img/default-org-logo.png'
