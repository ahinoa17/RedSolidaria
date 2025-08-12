# permutaciones/models.py
from django.db import models, transaction
from django.conf import settings
from django.utils import timezone
from django.core.exceptions import ValidationError
from oportunidades.models import OportunidadVoluntariado
from inscripciones.models import Inscripcion
from math import factorial

class SolicitudPermutacion(models.Model):
    """
    Modelo que representa una solicitud de permutación (intercambio) de turnos entre dos voluntarios.
    Utiliza el concepto de permutaciones para validar los intercambios posibles.
    """
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('aceptada', 'Aceptada'),
        ('rechazada', 'Rechazada'),
        ('cancelada', 'Cancelada')
    ]
    
    solicitante = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='solicitudes_enviadas',
        on_delete=models.CASCADE,
        verbose_name='Solicitante'
    )
    receptor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='solicitudes_recibidas',
        on_delete=models.CASCADE,
        verbose_name='Receptor'
    )
    oportunidad_origen = models.ForeignKey(
        OportunidadVoluntariado,
        related_name='solicitudes_salientes',
        on_delete=models.CASCADE,
        verbose_name='Oportunidad de origen'
    )
    oportunidad_destino = models.ForeignKey(
        OportunidadVoluntariado,
        related_name='solicitudes_entrantes',
        on_delete=models.CASCADE,
        verbose_name='Oportunidad de destino'
    )
    mensaje = models.TextField(blank=True, null=True, verbose_name='Mensaje')
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente', verbose_name='Estado')
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    fecha_actualizacion = models.DateTimeField(auto_now=True, verbose_name='Fecha de actualización')

    class Meta:
        verbose_name = 'solicitud de permutación'
        verbose_name_plural = 'solicitudes de permutación'
        ordering = ['-fecha_creacion']
        constraints = [
            models.UniqueConstraint(
                fields=['solicitante', 'receptor', 'oportunidad_origen', 'oportunidad_destino', 'estado'],
                name='solicitud_permutacion_unica',
                condition=models.Q(estado='pendiente')
            )
        ]

    def __str__(self):
        return f"Solicitud de {self.solicitante} a {self.receptor} ({self.get_estado_display()})"
    
    def clean(self):
        """
        Valida que la permutación sea posible antes de guardar.
        """
        super().clean()
        
        # No permitir auto-solicitudes
        if self.solicitante == self.receptor:
            raise ValidationError('No puedes enviar una solicitud a ti mismo')
        
        # Verificar que las oportunidades sean diferentes
        if self.oportunidad_origen == self.oportunidad_destino:
            raise ValidationError('Las oportunidades de origen y destino deben ser diferentes')
        
        # Verificar que el solicitante esté inscrito en la oportunidad de origen
        if not Inscripcion.objects.filter(
            usuario=self.solicitante, 
            oportunidad=self.oportunidad_origen,
            estado='aceptada'
        ).exists():
            raise ValidationError('Debes estar inscrito en la oportunidad de origen')
        
        # Verificar que el receptor esté inscrito en la oportunidad de destino
        if not Inscripcion.objects.filter(
            usuario=self.receptor, 
            oportunidad=self.oportunidad_destino,
            estado='aceptada'
        ).exists():
            raise ValidationError('El receptor debe estar inscrito en la oportunidad de destino')
        
        # Verificar que no exista una solicitud similar pendiente
        if self.estado == 'pendiente' and SolicitudPermutacion.objects.filter(
            solicitante=self.solicitante,
            receptor=self.receptor,
            oportunidad_origen=self.oportunidad_origen,
            oportunidad_destino=self.oportunidad_destino,
            estado='pendiente'
        ).exclude(pk=self.pk).exists():
            raise ValidationError('Ya existe una solicitud idéntica pendiente')
    
    @staticmethod
    def calcular_permutaciones_posibles(usuario, oportunidad_actual):
        """
        Calcula las permutaciones posibles para un usuario en una oportunidad específica.
        
        Args:
            usuario: El usuario que desea realizar la permutación
            oportunidad_actual: La oportunidad actual del usuario
            
        Returns:
            QuerySet: Oportunidades con las que se puede permutar
        """
        # Primero obtenemos los IDs de las oportunidades en las que el usuario ya está inscrito
        oportunidades_inscrito = Inscripcion.objects.filter(
            usuario=usuario,
            estado='aceptada'
        ).values_list('oportunidad_id', flat=True)
        
        # Luego obtenemos todas las oportunidades que cumplan con los criterios
        oportunidades_disponibles = OportunidadVoluntariado.objects.exclude(
            id=oportunidad_actual.id
        ).filter(
            # Que tengan cupos disponibles (asumiendo que el campo 'cupos' es el total de cupos)
            cupos__gt=0,
            # Que estén vigentes
            fecha_fin__gte=timezone.now().date(),
            # Que estén abiertas
            estado='abierta'
        ).exclude(
            # Excluir oportunidades en las que el usuario ya está inscrito
            id__in=oportunidades_inscrito
        )
        
        return oportunidades_disponibles
    
    @transaction.atomic
    def aceptar(self):
        """
        Acepta la solicitud de permutación y realiza el intercambio de turnos.
        Si el usuario ya está inscrito en la oportunidad de destino, rechaza automáticamente la solicitud.
        """
        if self.estado != 'pendiente':
            raise ValidationError('Solo se pueden aceptar solicitudes pendientes')
        
        with transaction.atomic():
            # Verificar si el solicitante ya está inscrito en la oportunidad de destino
            if Inscripcion.objects.filter(
                usuario=self.solicitante,
                oportunidad=self.oportunidad_destino
            ).exists():
                # Rechazar automáticamente la solicitud
                self.estado = 'rechazada'
                self.fecha_actualizacion = timezone.now()
                self.save()
                return 'rechazada', 'No se pudo completar el intercambio porque ya estás inscrito en la oportunidad de destino.'
            
            try:
                # Bloquear las filas para evitar condiciones de carrera
                inscripcion_receptor = Inscripcion.objects.select_for_update().get(
                    usuario=self.receptor,
                    oportunidad=self.oportunidad_destino,
                    estado='aceptada'
                )
                
                # Verificar que hay cupo en la oportunidad de origen
                if self.oportunidad_origen.cupos < 1:
                    return 'rechazada', 'Ya no hay cupo disponible en la oportunidad de origen.'
                
                # Obtener la inscripción actual del solicitante en la oportunidad de origen
                inscripcion_solicitante = Inscripcion.objects.get(
                    usuario=self.solicitante,
                    oportunidad=self.oportunidad_origen,
                    estado='aceptada'
                )
                
                # Actualizar la inscripción del solicitante a la nueva oportunidad
                inscripcion_solicitante.oportunidad = self.oportunidad_destino
                inscripcion_solicitante.comentarios = f'Intercambio aprobado de {self.oportunidad_origen.titulo} a {self.oportunidad_destino.titulo} el {timezone.now().strftime("%Y-%m-%d")}'
                
                # Verificar si el receptor ya está inscrito en la oportunidad de origen
                if Inscripcion.objects.filter(
                    usuario=self.receptor,
                    oportunidad=self.oportunidad_origen
                ).exists():
                    return 'rechazada', f'No se puede completar el intercambio porque {self.receptor.nombre_completo} ya está inscrito en la oportunidad de origen.'
                
                # Primero, actualizar la inscripción del receptor a la oportunidad de origen
                # Eliminamos la inscripción antigua y creamos una nueva para evitar problemas con la restricción única
                inscripcion_receptor.delete()
                
                # Crear una nueva inscripción para el receptor en la oportunidad de origen
                Inscripcion.objects.create(
                    usuario=self.receptor,
                    oportunidad=self.oportunidad_origen,
                    estado='aceptada',
                    comentarios=f'Intercambio aprobado de {self.oportunidad_destino.titulo} a {self.oportunidad_origen.titulo} el {timezone.now().strftime("%Y-%m-%d")}'
                )
                
                # Actualizar la inscripción del solicitante a la nueva oportunidad
                inscripcion_solicitante.oportunidad = self.oportunidad_destino
                inscripcion_solicitante.comentarios = f'Intercambio aprobado de {self.oportunidad_origen.titulo} a {self.oportunidad_destino.titulo} el {timezone.now().strftime("%Y-%m-%d")}'
                inscripcion_solicitante.save()
                
                # Actualizar cupos
                self.oportunidad_origen.cupos += 1  # Aumentar cupos en origen (donde va el receptor)
                self.oportunidad_destino.cupos -= 1  # Disminuir cupos en destino (donde va el solicitante)
                
                # Guardar cambios en las oportunidades
                self.oportunidad_origen.save()
                self.oportunidad_destino.save()
                
                # Marcar la solicitud como aceptada
                self.estado = 'aceptada'
                self.fecha_actualizacion = timezone.now()
                self.save()
                
                # Rechazar automáticamente otras solicitudes pendientes para estas inscripciones
                from django.db.models import Q
                
                return 'aceptada', 'El intercambio se ha realizado con éxito.'
                
            except Inscripcion.DoesNotExist as e:
                # Si no se encuentra alguna inscripción necesaria
                return 'rechazada', 'No se pudo completar el intercambio. Una de las inscripciones necesarias no existe.'
            except Exception as e:
                # Para cualquier otro error inesperado
                return 'error', f'Error inesperado: {str(e)}'
            
            # Obtener todas las solicitudes pendientes que involucren a estos usuarios y oportunidades
            solicitudes_a_rechazar = SolicitudPermutacion.objects.filter(
                models.Q(estado='pendiente') &
                ~models.Q(pk=self.pk) &
                (
                    (models.Q(solicitante=self.solicitante) & models.Q(oportunidad_origen=self.oportunidad_origen)) |
                    (models.Q(solicitante=self.receptor) & models.Q(oportunidad_origen=self.oportunidad_destino)) |
                    (models.Q(receptor=self.solicitante) & models.Q(oportunidad_destino=self.oportunidad_origen)) |
                    (models.Q(receptor=self.receptor) & models.Q(oportunidad_destino=self.oportunidad_destino))
                )
            )
            
            # Actualizar todas las solicitudes encontradas
            solicitudes_a_rechazar.update(
                estado='rechazada',
                fecha_actualizacion=timezone.now()
            )
    
    def rechazar(self):
        """
        Rechaza la solicitud de permutación.
        """
        if self.estado != 'pendiente':
            raise ValidationError('Solo se pueden rechazar solicitudes pendientes')
            
        self.estado = 'rechazada'
        self.fecha_actualizacion = timezone.now()
        self.save()
    
    def cancelar(self):
        """
        Cancela la solicitud de permutación.
        """
        if self.estado != 'pendiente':
            raise ValidationError('Solo se pueden cancelar solicitudes pendientes')
            
        self.estado = 'cancelada'
        self.fecha_actualizacion = timezone.now()
        self.save()