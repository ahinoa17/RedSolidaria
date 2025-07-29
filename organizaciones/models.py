from django.db import models

class Organizacion(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    contacto_email = models.EmailField()
    telefono = models.CharField(max_length=20, blank=True)
    direccion = models.CharField(max_length=255, blank=True)
    fecha_creacion = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.nombre
