from django.db import models
from oportunidades.models import OportunidadVoluntariado

class PermutacionParticipantes(models.Model):
    oportunidad = models.ForeignKey(OportunidadVoluntariado, on_delete=models.CASCADE)
    total_participantes = models.PositiveIntegerField()
    resultado_permutacion = models.BigIntegerField()
    fecha_calculo = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Permutaciones para {self.oportunidad.titulo}: {self.resultado_permutacion}"