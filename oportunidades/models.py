# Importa el módulo models de Django para definir los modelos
from django.db import models
# Importa el modelo Organizacion para la relación ForeignKey
from organizaciones.models import Organizacion

class OportunidadVoluntariado(models.Model):
    """Modelo que representa una oportunidad de voluntariado."""
    
    # Campo de texto corto para el título
    titulo = models.CharField(max_length=150)
    
    # Campo de texto largo para la descripción
    descripcion = models.TextField()
    
    # Fecha de inicio de la oportunidad
    fecha_inicio = models.DateField()
    
    # Fecha de finalización de la oportunidad
    fecha_fin = models.DateField()
    
    # Relación muchos a uno con el modelo Organizacion
    organizacion = models.ForeignKey(Organizacion, on_delete=models.CASCADE)
    
    # Ubicación donde se realizará el voluntariado
    ubicacion = models.CharField(max_length=255)
    
    # Número de cupos disponibles (entero positivo)
    cupos = models.PositiveIntegerField()
    
    # Estado de la oportunidad con opciones predefinidas
    estado = models.CharField(
        max_length=20, 
        choices=[('abierta', 'Abierta'), ('cerrada', 'Cerrada')], 
        default='abierta'
    )
    
    # Fecha de creación automática
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    # Horario del voluntariado
    horario = models.CharField(
        max_length=100, 
        help_text="Ej: Lunes a Viernes, 9:00 AM - 5:00 PM",
        blank=True,
        default=''
    )
    
    # Requisitos para participar
    requisitos = models.TextField(
        help_text="Lista los requisitos necesarios para el voluntariado",
        blank=True,
        default=''
    )
    
    # Beneficios que ofrece la oportunidad
    beneficios = models.TextField(
        help_text="Describe los beneficios que ofrece el voluntariado",
        blank=True,
        default=''
    )

    def __str__(self):
        """Representación en cadena del objeto (para el admin y shell)."""
        return self.titulo  

    class Meta:
        """Metadatos del modelo."""
        # Nombre singular en el admin
        verbose_name = "Oportunidad de Voluntariado"
        
        # Nombre plural en el admin
        verbose_name_plural = "Oportunidades de Voluntariado"
        
        # Orden por defecto (más recientes primero)
        ordering = ['-fecha_creacion']