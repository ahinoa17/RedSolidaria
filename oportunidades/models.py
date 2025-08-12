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
    estado = models.CharField(
        max_length=20, 
        choices=[('abierta', 'Abierta'), ('cerrada', 'Cerrada')], 
        default='abierta'
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    horario = models.CharField(
        max_length=100, 
        help_text="Ej: Lunes a Viernes, 9:00 AM - 5:00 PM",
        blank=True,
        default=''
    )
    requisitos = models.TextField(
        help_text="Lista los requisitos necesarios para el voluntariado",
        blank=True,
        default=''
    )
    beneficios = models.TextField(
        help_text="Describe los beneficios que ofrece el voluntariado",
        blank=True,
        default=''
    )

    def __str__(self):
        return self.titulo  

    class Meta:
        verbose_name = "Oportunidad de Voluntariado"
        verbose_name_plural = "Oportunidades de Voluntariado"
        ordering = ['-fecha_creacion']  # Ordena por fecha de creación descendente