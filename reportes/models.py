from django.db import models
from django.contrib.auth.models import User
from oportunidades.models import OportunidadVoluntariado

class ReporteParticipacion(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    oportunidad = models.ForeignKey(OportunidadVoluntariado, on_delete=models.CASCADE)
    horas = models.PositiveIntegerField()
    feedback = models.TextField(blank=True)
    fecha_reporte = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reporte de {self.usuario.username} en {self.oportunidad.titulo}"
