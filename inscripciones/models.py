from django.db import models
from django.contrib.auth.models import User
from oportunidades.models import OportunidadVoluntariado

class Inscripcion(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    oportunidad = models.ForeignKey(OportunidadVoluntariado, on_delete=models.CASCADE)
    fecha_inscripcion = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=[('pendiente', 'Pendiente'), ('aceptada', 'Aceptada'), ('rechazada', 'Rechazada')], default='pendiente')
    comentarios = models.TextField(blank=True)

    def __str__(self):
        return f"{self.usuario.username} - {self.oportunidad.titulo}"