from django.db import models
from django.conf import settings
from oportunidades.models import OportunidadVoluntariado

class Inscripcion(models.Model):
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('aceptada', 'Aceptada'),
        ('rechazada', 'Rechazada'),
        ('completada', 'Completada'),
    ]

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='usuario'
    )
    oportunidad = models.ForeignKey(
        OportunidadVoluntariado,
        on_delete=models.CASCADE,
        related_name='inscripciones',
        verbose_name='oportunidad'
    )
    fecha_inscripcion = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(
        max_length=20,
        choices=ESTADOS,
        default='pendiente'
    )
    comentarios = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = 'inscripción'
        verbose_name_plural = 'inscripciones'
        unique_together = ['usuario', 'oportunidad']
    
    def __str__(self):
        return f"Inscripción de {self.usuario.email} a {self.oportunidad.titulo}"
