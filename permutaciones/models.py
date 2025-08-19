# Importaciones necesarias para el modelo
from django.db import models, transaction
from django.conf import settings
from django.utils import timezone
from django.core.exceptions import ValidationError
from oportunidades.models import OportunidadVoluntariado
from inscripciones.models import Inscripcion
from math import factorial
from django.contrib.auth import get_user_model

class SolicitudPermutacion(models.Model):
    """
    Modelo que representa una solicitud de permutación (intercambio) de turnos entre dos voluntarios.
    Utiliza el concepto de permutaciones para validar los intercambios posibles.
    """
    
    # Opciones para el campo estado
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('aceptada', 'Aceptada'),
        ('rechazada', 'Rechazada'),
        ('cancelada', 'Cancelada')
    ]
    
    # Relación con el usuario que envía la solicitud
    solicitante = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='solicitudes_enviadas',
        on_delete=models.CASCADE,
        verbose_name='Solicitante'
    )
    
    # Relación con el usuario que recibe la solicitud
    receptor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='solicitudes_recibidas',
        on_delete=models.CASCADE,
        verbose_name='Receptor'
    )
    
    # Oportunidad de origen del intercambio
    oportunidad_origen = models.ForeignKey(
        OportunidadVoluntariado,
        related_name='solicitudes_salientes',
        on_delete=models.CASCADE,
        verbose_name='Oportunidad de origen'
    )
    
    # Oportunidad de destino del intercambio
    oportunidad_destino = models.ForeignKey(
        OportunidadVoluntariado,
        related_name='solicitudes_entrantes',
        on_delete=models.CASCADE,
        verbose_name='Oportunidad de destino'
    )
    
    # Mensaje opcional que acompaña a la solicitud
    mensaje = models.TextField(blank=True, null=True, verbose_name='Mensaje')
    
    # Estado actual de la solicitud
    estado = models.CharField(
        max_length=20, 
        choices=ESTADOS, 
        default='pendiente', 
        verbose_name='Estado'
    )
    
    # Fecha de creación de la solicitud
    fecha_creacion = models.DateTimeField(
        auto_now_add=True, 
        verbose_name='Fecha de creación'
    )
    
    # Fecha de última actualización
    fecha_actualizacion = models.DateTimeField(
        auto_now=True, 
        verbose_name='Fecha de actualización'
    )

    class Meta:
        # Configuración de metadatos del modelo
        verbose_name = 'solicitud de permutación'
        verbose_name_plural = 'solicitudes de permutación'
        ordering = ['-fecha_creacion']
        
        # Restricción para evitar solicitudes duplicadas
        constraints = [
            models.UniqueConstraint(
                fields=['solicitante', 'receptor', 'oportunidad_origen', 'oportunidad_destino', 'estado'],
                name='solicitud_permutacion_unica',
                condition=models.Q(estado='pendiente')
            )
        ]

    def __str__(self):
        """Representación en cadena de la solicitud"""
        return f"Intercambio de {self.solicitante} ({self.oportunidad_origen} -> {self.oportunidad_destino})"

    def save(self, *args, **kwargs):
        """
        Sobrescribes el método save para registrar automáticamente la creación de la solicitud.
        """
        # Verificar si es una creación nueva (no tiene ID aún)
        is_new = self._state.adding
        
        # Guardar la instancia
        super().save(*args, **kwargs)
        
        # Si es una creación nueva, registrar en el historial
        if is_new:
            # Obtener el usuario actual del request si está disponible
            user = getattr(self, '_usuario_actual', None)
            
            detalles = (
                f"NUEVA SOLICITUD DE INTERCAMBIO\n"
                f"• Solicitante: {self.solicitante.get_full_name() or self.solicitante.email}\n"
                f"• Receptor: {self.receptor.get_full_name() or self.receptor.email}\n"
                f"• Oportunidad Origen: {self.oportunidad_origen.titulo} (ID: {self.oportunidad_origen.id})\n"
                f"• Oportunidad Destino: {self.oportunidad_destino.titulo} (ID: {self.oportunidad_destino.id})\n"
                f"• Mensaje: {self.mensaje or 'Sin mensaje'}\n"
                f"• Fecha: {self.fecha_creacion.strftime('%d/%m/%Y %H:%M')}"
            )
            
            HistorialPermutacion.objects.create(
                solicitud=self,
                accion='creacion',
                detalles=detalles,
                usuario=user
            )

    def clean(self):
        """
        Valida que la permutación sea posible antes de guardar.
        Realiza validaciones de integridad de datos.
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
        Devuelve información detallada de los usuarios con los que se puede intercambiar.
        
        Args:
            usuario: El usuario que desea realizar la permutación
            oportunidad_actual: La oportunidad actual del usuario
            
        Returns:
            list: Lista de diccionarios con información detallada de las oportunidades
                  y usuarios disponibles para intercambio
        """
        # Obtener la inscripción actual del usuario
        try:
            inscripcion_actual = Inscripcion.objects.get(
                usuario=usuario,
                oportunidad=oportunidad_actual,
                estado='aceptada'
            )
        except Inscripcion.DoesNotExist:
            return []

        # Obtener todas las oportunidades disponibles para intercambio
        # que no sean la actual, que estén abiertas y con cupos disponibles
        oportunidades_disponibles = OportunidadVoluntariado.objects.filter(
            fecha_fin__gte=timezone.now().date(),  # Oportunidades vigentes
            estado='abierta',
            cupos__gt=0  # Con cupos disponibles
        ).exclude(
            id=oportunidad_actual.id  # Excluir la oportunidad actual
        ).select_related('organizacion')

        # Lista para almacenar las oportunidades con usuarios disponibles
        oportunidades_con_usuarios = []

        for oportunidad in oportunidades_disponibles:
            # Buscar usuarios inscritos en esta oportunidad que podrían intercambiar
            usuarios_disponibles = Inscripcion.objects.filter(
                oportunidad=oportunidad,
                estado='aceptada'
            ).exclude(
                usuario=usuario  # Excluir al usuario actual
            ).select_related('usuario')

            # Verificar que el usuario no esté ya en esta oportunidad
            if Inscripcion.objects.filter(
                usuario=usuario,
                oportunidad=oportunidad,
                estado='aceptada'
            ).exists():
                continue  # Saltar esta oportunidad si el usuario ya está inscrito


            # Filtrar usuarios que no estén en la oportunidad actual
            usuarios_filtrados = []
            for usuario_disp in usuarios_disponibles:
                # Verificar que el usuario no esté ya en la oportunidad actual
                if not Inscripcion.objects.filter(
                    usuario=usuario_disp.usuario,
                    oportunidad=oportunidad_actual
                ).exists():
                    # Acceder a los campos directamente del modelo Usuario
                    usuarios_filtrados.append({
                        'id': usuario_disp.usuario.id,
                        'nombre_completo': usuario_disp.usuario.get_full_name() or usuario_disp.usuario.email,
                        'email': usuario_disp.usuario.email,
                        'telefono': usuario_disp.usuario.telefono or 'No disponible',
                        'foto_perfil': None,  # No hay campo de foto en el modelo actual
                        'fecha_inscripcion': usuario_disp.fecha_inscripcion
                    })

            if usuarios_filtrados:
                # Verificar que la oportunidad tenga organización asociada
                org_nombre = 'Sin organización'
                org_logo = None
                
                if hasattr(oportunidad, 'organizacion') and oportunidad.organizacion:
                    org_nombre = oportunidad.organizacion.nombre
                    if hasattr(oportunidad.organizacion, 'logo') and oportunidad.organizacion.logo:
                        try:
                            org_logo = oportunidad.organizacion.logo.url
                        except:
                            org_logo = None
                
                oportunidades_con_usuarios.append({
                    'oportunidad': {
                        'id': oportunidad.id,
                        'titulo': oportunidad.titulo,
                        'descripcion': oportunidad.descripcion,
                        'fecha_inicio': oportunidad.fecha_inicio,
                        'fecha_fin': oportunidad.fecha_fin,
                        'ubicacion': oportunidad.ubicacion,
                        'organizacion': {
                            'nombre': org_nombre,
                            'logo': org_logo
                        }
                    },
                    'usuarios_disponibles': usuarios_filtrados
                })

        return oportunidades_con_usuarios
    
    @transaction.atomic
    def aceptar(self):
        """
        Acepta la solicitud de permutación y realiza el intercambio de turnos.
        Maneja la transacción atómicamente para mantener la integridad de los datos.
        """
        if self.estado != 'pendiente':
            raise ValidationError('Solo se pueden aceptar solicitudes pendientes')
            
        with transaction.atomic():
            try:
                # Obtener el usuario que realiza la acción
                usuario_accion = getattr(self, '_usuario_actual', None)
                
                # Verificar si el solicitante ya está en la oportunidad de destino
                if Inscripcion.objects.filter(usuario=self.solicitante, oportunidad=self.oportunidad_destino).exists():
                    self.estado = 'rechazada'
                    self.fecha_actualizacion = timezone.now()
                    self.save()
                    
                    # Crear registro detallado del rechazo
                    detalles = (
                        f"INTERCAMBIO RECHAZADO AUTOMÁTICAMENTE\n"
                        f"• Motivo: El solicitante ya está inscrito en la oportunidad de destino\n"
                        f"• Solicitante: {self.solicitante.get_full_name() or self.solicitante.email}\n"
                        f"• Oportunidad Destino: {self.oportunidad_destino.titulo} (ID: {self.oportunidad_destino.id})\n"
                        f"• Fecha: {self.fecha_actualizacion.strftime('%d/%m/%Y %H:%M')}\n"
                        f"• Acción realizada por: {usuario_accion.get_full_name() if usuario_accion else 'Sistema'}"
                    )
                    
                    HistorialPermutacion.objects.create(
                        solicitud=self,
                        accion='rechazo',
                        detalles=detalles,
                        usuario=usuario_accion
                    )
                    raise ValidationError('El solicitante ya está inscrito en la oportunidad de destino')
                    
                # Verificar si el receptor ya está en la oportunidad de origen
                if Inscripcion.objects.filter(usuario=self.receptor, oportunidad=self.oportunidad_origen).exists():
                    self.estado = 'rechazada'
                    self.fecha_actualizacion = timezone.now()
                    self.save()
                    
                    # Crear registro detallado del rechazo
                    detalles = (
                        f"INTERCAMBIO RECHAZADO AUTOMÁTICAMENTE\n"
                        f"• Motivo: El receptor ya está inscrito en la oportunidad de origen\n"
                        f"• Receptor: {self.receptor.get_full_name() or self.receptor.email}\n"
                        f"• Oportunidad Origen: {self.oportunidad_origen.titulo} (ID: {self.oportunidad_origen.id})\n"
                        f"• Fecha: {self.fecha_actualizacion.strftime('%d/%m/%Y %H:%M')}\n"
                        f"• Acción realizada por: {usuario_accion.get_full_name() if usuario_accion else 'Sistema'}"
                    )
                    
                    HistorialPermutacion.objects.create(
                        solicitud=self,
                        accion='rechazo',
                        detalles=detalles,
                        usuario=usuario_accion
                    )
                    raise ValidationError('El receptor ya está inscrito en la oportunidad de origen')
                    
                # Obtener las inscripciones
                inscripcion_solicitante = Inscripcion.objects.get(
                    usuario=self.solicitante,
                    oportunidad=self.oportunidad_origen,
                    estado='aceptada'
                )
                
                inscripcion_receptor = Inscripcion.objects.get(
                    usuario=self.receptor,
                    oportunidad=self.oportunidad_destino,
                    estado='aceptada'
                )
                
                # Guardar información para el historial
                info_intercambio = (
                    f"INTERCAMBIO REALIZADO CON ÉXITO\n"
                    f"• Solicitante: {self.solicitante.get_full_name() or self.solicitante.email}\n"
                    f"• Receptor: {self.receptor.get_full_name() or self.receptor.email}\n"
                    f"• Oportunidad Origen: {self.oportunidad_origen.titulo} (ID: {self.oportunidad_origen.id})\n"
                    f"• Oportunidad Destino: {self.oportunidad_destino.titulo} (ID: {self.oportunidad_destino.id})\n"
                    f"• Fecha: {timezone.now().strftime('%d/%m/%Y %H:%M')}\n"
                    f"• Acción realizada por: {usuario_accion.get_full_name() if usuario_accion else 'Sistema'}\n"
                    f"• Detalles del Intercambio:\n"
                    f"  - {self.solicitante.get_short_name()}: {self.oportunidad_origen.titulo} → {self.oportunidad_destino.titulo}\n"
                    f"  - {self.receptor.get_short_name()}: {self.oportunidad_destino.titulo} → {self.oportunidad_origen.titulo}"
                )
                
                # Realizar el intercambio
                inscripcion_solicitante.oportunidad = self.oportunidad_destino
                inscripcion_solicitante.fecha_actualizacion = timezone.now()
                inscripcion_solicitante.save()
                
                inscripcion_receptor.oportunidad = self.oportunidad_origen
                inscripcion_receptor.fecha_actualizacion = timezone.now()
                inscripcion_receptor.save()
                
                # Actualizar el estado de la solicitud
                self.estado = 'aceptada'
                self.fecha_actualizacion = timezone.now()
                self.save()
                
                # Registrar la aceptación en el historial
                HistorialPermutacion.objects.create(
                    solicitud=self,
                    accion='aceptacion',
                    detalles=info_intercambio,
                    usuario=usuario_accion
                )
                
                # Rechazar otras solicitudes pendientes conflictivas
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
                
                # Crear registros de historial para las solicitudes rechazadas automáticamente
                for solicitud in solicitudes_a_rechazar:
                    detalles_rechazo = (
                        f"INTERCAMBIO RECHAZADO AUTOMÁTICAMENTE\n"
                        f"• Motivo: Otra solicitud de intercambio fue aceptada para las mismas oportunidades\n"
                        f"• Solicitante: {solicitud.solicitante.get_full_name() or solicitud.solicitante.email}\n"
                        f"• Oportunidad Origen: {solicitud.oportunidad_origen.titulo} (ID: {solicitud.oportunidad_origen.id})\n"
                        f"• Oportunidad Destino: {solicitud.oportunidad_destino.titulo} (ID: {solicitud.oportunidad_destino.id})\n"
                        f"• Fecha: {timezone.now().strftime('%d/%m/%Y %H:%M')}\n"
                        f"• Acción realizada por: {usuario_accion.get_full_name() if usuario_accion else 'Sistema'}"
                    )
                    
                    HistorialPermutacion.objects.create(
                        solicitud=solicitud,
                        accion='rechazo',
                        detalles=detalles_rechazo,
                        usuario=usuario_accion
                    )
                
                # Actualizar el estado de las solicitudes rechazadas
                solicitudes_a_rechazar.update(
                    estado='rechazada',
                    fecha_actualizacion=timezone.now()
                )
                
                return 'aceptada', 'Intercambio realizado con éxito.'
                
            except Inscripcion.DoesNotExist:
                # Registrar el error en el historial
                detalles_error = (
                    f"ERROR EN INTERCAMBIO\n"
                    f"• Motivo: No se pudo completar el intercambio. Una de las inscripciones necesarias no existe.\n"
                    f"• Solicitante: {self.solicitante.get_full_name() or self.solicitante.email}\n"
                    f"• Receptor: {self.receptor.get_full_name() or self.receptor.email}\n"
                    f"• Oportunidad Origen: {self.oportunidad_origen.titulo} (ID: {self.oportunidad_origen.id})\n"
                    f"• Oportunidad Destino: {self.oportunidad_destino.titulo} (ID: {self.oportunidad_destino.id})\n"
                    f"• Fecha: {timezone.now().strftime('%d/%m/%Y %H:%M')}"
                )
                
                HistorialPermutacion.objects.create(
                    solicitud=self,
                    accion='error',
                    detalles=detalles_error,
                    usuario=usuario_accion
                )
                
                self.estado = 'rechazada'
                self.fecha_actualizacion = timezone.now()
                self.save()
                
                return 'rechazada', 'No se pudo completar el intercambio. Una de las inscripciones necesarias no existe.'
                
            except Exception as e:
                # Registrar el error en el historial
                detalles_error = (
                    f"ERROR EN INTERCAMBIO\n"
                    f"• Motivo: Error inesperado: {str(e)}\n"
                    f"• Solicitante: {self.solicitante.get_full_name() or self.solicitante.email}\n"
                    f"• Receptor: {self.receptor.get_full_name() or self.receptor.email}\n"
                    f"• Oportunidad Origen: {self.oportunidad_origen.titulo} (ID: {self.oportunidad_origen.id})\n"
                    f"• Oportunidad Destino: {self.oportunidad_destino.titulo} (ID: {self.oportunidad_destino.id})\n"
                    f"• Fecha: {timezone.now().strftime('%d/%m/%Y %H:%M')}"
                )
                
                HistorialPermutacion.objects.create(
                    solicitud=self,
                    accion='error',
                    detalles=detalles_error,
                    usuario=usuario_accion
                )
                
                self.estado = 'rechazada'
                self.fecha_actualizacion = timezone.now()
                self.save()
                
                return 'error', f'Error inesperado: {str(e)}'
    
    def rechazar(self):
        """
        Rechaza la solicitud de permutación.
        Actualiza el estado a 'rechazada' y la fecha de actualización.
        """
        if self.estado != 'pendiente':
            raise ValidationError('Solo se pueden rechazar solicitudes pendientes')
            
        self.estado = 'rechazada'
        self.fecha_actualizacion = timezone.now()
        self.save()
        
        # Obtener el usuario que realiza la acción
        usuario_accion = getattr(self, '_usuario_actual', None)
        
        # Registrar el rechazo en el historial con detalles
        detalles = (
            f"INTERCAMBIO RECHAZADO\n"
            f"• Solicitante: {self.solicitante.get_full_name() or self.solicitante.email}\n"
            f"• Receptor: {self.receptor.get_full_name() or self.receptor.email}\n"
            f"• Oportunidad Origen: {self.oportunidad_origen.titulo} (ID: {self.oportunidad_origen.id})\n"
            f"• Oportunidad Destino: {self.oportunidad_destino.titulo} (ID: {self.oportunidad_destino.id})\n"
            f"• Fecha: {self.fecha_actualizacion.strftime('%d/%m/%Y %H:%M')}\n"
            f"• Acción realizada por: {usuario_accion.get_full_name() if usuario_accion else 'Sistema'}"
        )
        
        HistorialPermutacion.objects.create(
            solicitud=self,
            accion='rechazo',
            detalles=detalles,
            usuario=usuario_accion
        )
    
    def cancelar(self):
        """
        Cancela la solicitud de permutación.
        Actualiza el estado a 'cancelada' y la fecha de actualización.
        """
        if self.estado != 'pendiente':
            raise ValidationError('Solo se pueden cancelar solicitudes pendientes')
            
        self.estado = 'cancelada'
        self.fecha_actualizacion = timezone.now()
        self.save()
        
        # Obtener el usuario que realiza la acción
        usuario_accion = getattr(self, '_usuario_actual', None)
        
        # Registrar la cancelación en el historial con detalles
        detalles = (
            f"INTERCAMBIO CANCELADO\n"
            f"• Solicitante: {self.solicitante.get_full_name() or self.solicitante.email}\n"
            f"• Receptor: {self.receptor.get_full_name() or self.receptor.email}\n"
            f"• Oportunidad Origen: {self.oportunidad_origen.titulo} (ID: {self.oportunidad_origen.id})\n"
            f"• Oportunidad Destino: {self.oportunidad_destino.titulo} (ID: {self.oportunidad_destino.id})\n"
            f"• Fecha: {self.fecha_actualizacion.strftime('%d/%m/%Y %H:%M')}\n"
            f"• Acción realizada por: {usuario_accion.get_full_name() if usuario_accion else 'Sistema'}\n"
            f"• Razón: Cancelación por el solicitante"
        )
        
        HistorialPermutacion.objects.create(
            solicitud=self,
            accion='cancelacion',
            detalles=detalles,
            usuario=usuario_accion
        )


class HistorialPermutacion(models.Model):
    """
    Modelo para registrar el historial de cambios en las solicitudes de permutación.
    Solo visible para superusuarios en el admin.
    """
    TIPOS_ACCION = [
        ('creacion', 'Creación de Solicitud'),
        ('aceptacion', 'Aceptación de Intercambio'),
        ('rechazo', 'Rechazo de Solicitud'),
        ('cancelacion', 'Cancelación de Solicitud'),
    ]
    
    solicitud = models.ForeignKey(
        SolicitudPermutacion,
        on_delete=models.CASCADE,
        related_name='historial',
        verbose_name='Solicitud de Permutación'
    )
    accion = models.CharField(
        max_length=20,
        choices=TIPOS_ACCION,
        verbose_name='Tipo de Acción'
    )
    detalles = models.TextField(
        verbose_name='Detalles del Cambio',
        help_text='Información detallada sobre el cambio realizado'
    )
    fecha = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha del Cambio'
    )
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Usuario que realizó la acción'
    )

    @property
    def detalles_lines(self):
        """
        Devuelve los detalles divididos en líneas para facilitar el formateo en plantillas.
        """
        if not hasattr(self, '_detalles_lines'):
            self._detalles_lines = self.detalles.split('\n') if self.detalles else []
        return self._detalles_lines

    def __str__(self):
        """
        Representación en cadena del registro de historial.
        """
        return f"{self.get_accion_display()} - {self.fecha.strftime('%d/%m/%Y %H:%M')}"

    class Meta:
        verbose_name = 'Historial de Permutación'
        verbose_name_plural = 'Historial de Permutaciones'
        ordering = ['-fecha']
        permissions = [
            ('view_historial_permutacion', 'Puede ver el historial de permutaciones'),
        ]