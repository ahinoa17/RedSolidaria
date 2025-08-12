from django.db import models
from django.utils.text import slugify

class Organizacion(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField()
    contacto_email = models.EmailField()
    telefono = models.CharField(max_length=20, blank=True)
    direccion = models.CharField(max_length=255, blank=True)
    logo = models.CharField(max_length=100, blank=True, help_text='Nombre del archivo del logo en static/img/logos/')
    activa = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre

    @property
    def logo_url(self):
        if self.logo:
            return f'/static/img/logos/{self.logo}'
        return '/static/img/default-org-logo.png'
