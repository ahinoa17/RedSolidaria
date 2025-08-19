# Importa los modelos de Django
from django.db import models
# Importa la configuración de Django
from django.conf import settings
# Importa el modelo OportunidadVoluntariado de la app oportunidades
from oportunidades.models import OportunidadVoluntariado


# Define el modelo Inscripcion que hereda de models.Model
class Inscripcion(models.Model):
    # Lista de tuplas que define los estados posibles de una inscripción
    # Formato: (valor_guardado, texto_mostrado)
    ESTADOS = [
        ('pendiente', 'Pendiente'),  # Estado inicial de la inscripción
        ('aceptada', 'Aceptada'),    # Inscripción aprobada
        ('rechazada', 'Rechazada'),  # Inscripción denegada
        ('completada', 'Completada'),# Actividad finalizada
    ]

    # Campo que relaciona con el modelo de Usuario
    # CASCADE: si se borra el usuario, se borran sus inscripciones
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # Usa el modelo de usuario definido en settings
        on_delete=models.CASCADE,  # Comportamiento al eliminar el usuario relacionado
        verbose_name='usuario'     # Nombre legible en el admin
    )
    
    # Campo que relaciona con el modelo OportunidadVoluntariado
    oportunidad = models.ForeignKey(
        OportunidadVoluntariado,  # Modelo relacionado
        on_delete=models.CASCADE,  # Si se borra la oportunidad, se borran sus inscripciones
        related_name='inscripciones',  # Nombre para acceder desde OportunidadVoluntariado
        verbose_name='oportunidad'     # Nombre legible en el admin
    )
    
    # Fecha de inscripción que se establece automáticamente al crear el registro
    fecha_inscripcion = models.DateTimeField(auto_now_add=True)
    
    # Campo para el estado de la inscripción
    estado = models.CharField(
        max_length=20,           # Longitud máxima del texto
        choices=ESTADOS,         # Usa las opciones definidas en ESTADOS
        default='pendiente'      # Valor por defecto al crear una nueva inscripción
    )
    
    # Campo de texto opcional para comentarios
    # blank=True: permite campo vacío en formularios
    # null=True: permite NULL en la base de datos
    comentarios = models.TextField(blank=True, null=True)

    # Clase Meta para metadatos del modelo
    class Meta:
        verbose_name = 'inscripción'           # Nombre singular en el admin
        verbose_name_plural = 'inscripciones'  # Nombre plural en el admin
        # Evita que un usuario se inscriba dos veces a la misma oportunidad
        unique_together = ['usuario', 'oportunidad']
    
    # Método que devuelve una representación en string del objeto
    def __str__(self):
        # Muestra el email del usuario y el título de la oportunidad
        return f"Inscripción de {self.usuario.email} a {self.oportunidad.titulo}"