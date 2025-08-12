from django.db import models
from django.conf import settings
from oportunidades.models import OportunidadVoluntariado

class ReporteParticipacion(models.Model):
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='usuario'
    )
    oportunidad = models.ForeignKey(
        OportunidadVoluntariado,
        on_delete=models.CASCADE,
        verbose_name='oportunidad'
    )
    fecha_reporte = models.DateField()
    horas = models.DecimalField(max_digits=5, decimal_places=2)
    descripcion = models.TextField()
    evidencia = models.FileField(upload_to='reportes/evidencias/', blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'reporte de participación'
        verbose_name_plural = 'reportes de participación'
    
    def __str__(self):
        return f"Reporte de {self.usuario.email} - {self.oportunidad.titulo} ({self.fecha_reporte})"
