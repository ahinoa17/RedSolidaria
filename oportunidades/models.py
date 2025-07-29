from django.db import models
from organizaciones.models import Organizacion

class OportunidadVoluntariado(models.Model):
    titulo = models.CharField(max_length=150)
    descripcion = models.TextField()
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    organizacion = models.ForeignKey(Organizacion, on_delete=models.CASCADE)
    ubicacion = models.CharField(max_length=255)
    cupos = models.PositiveIntegerField()
    estado = models.CharField(max_length=20, choices=[('abierta', 'Abierta'), ('cerrada', 'Cerrada')], default='abierta')
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo
