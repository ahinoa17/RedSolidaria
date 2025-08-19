from django.core.management.base import BaseCommand
from permutaciones.models import SolicitudPermutacion, HistorialPermutacion
from django.utils import timezone

class Command(BaseCommand):
    help = 'Crea registros de historial para solicitudes de permutación existentes'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force-update',
            action='store_true',
            help='Forzar la actualización de todos los registros de historial existentes',
        )

    def handle(self, *args, **options):
        force_update = options.get('force_update', False)
        # Obtener todas las solicitudes existentes
        solicitudes = SolicitudPermutacion.objects.all()
        
        for solicitud in solicitudes:
            # Determinar el tipo de acción basado en el estado
            if solicitud.estado == 'aceptada':
                accion = 'aceptacion'
                detalles = (
                    f"INTERCAMBIO ACEPTADO\n"
                    f"• Solicitante: {solicitud.solicitante.get_full_name() or solicitud.solicitante.email}\n"
                    f"• Receptor: {solicitud.receptor.get_full_name() or solicitud.receptor.email}\n"
                    f"• Oportunidad Origen: {solicitud.oportunidad_origen.titulo}\n"
                    f"• Oportunidad Destino: {solicitud.oportunidad_destino.titulo}\n"
                    f"• Fecha: {timezone.localtime(solicitud.fecha_actualizacion).strftime('%d/%m/%Y %H:%M')}\n"
                    f"• Detalles del Intercambio:\n"
                    f"  - {solicitud.solicitante.get_short_name()}: {solicitud.oportunidad_origen.titulo} → {solicitud.oportunidad_destino.titulo}\n"
                    f"  - {solicitud.receptor.get_short_name()}: {solicitud.oportunidad_destino.titulo} → {solicitud.oportunidad_origen.titulo}"
                )
            elif solicitud.estado == 'rechazada':
                accion = 'rechazo'
                detalles = (
                    f"INTERCAMBIO RECHAZADO\n"
                    f"• Solicitante: {solicitud.solicitante.get_full_name() or solicitud.solicitante.email}\n"
                    f"• Receptor: {solicitud.receptor.get_full_name() or solicitud.receptor.email}\n"
                    f"• Oportunidad Origen: {solicitud.oportunidad_origen.titulo}\n"
                    f"• Oportunidad Destino: {solicitud.oportunidad_destino.titulo}\n"
                    f"• Fecha: {timezone.localtime(solicitud.fecha_actualizacion).strftime('%d/%m/%Y %H:%M')}\n"
                    f"• Acción realizada por: Sistema (actualización automática)"
                )
            elif solicitud.estado == 'cancelada':
                accion = 'cancelacion'
                detalles = (
                    f"INTERCAMBIO CANCELADO\n"
                    f"• Solicitante: {solicitud.solicitante.get_full_name() or solicitud.solicitante.email}\n"
                    f"• Receptor: {solicitud.receptor.get_full_name() or solicitud.receptor.email}\n"
                    f"• Oportunidad Origen: {solicitud.oportunidad_origen.titulo}\n"
                    f"• Oportunidad Destino: {solicitud.oportunidad_destino.titulo}\n"
                    f"• Fecha: {timezone.localtime(solicitud.fecha_actualizacion).strftime('%d/%m/%Y %H:%M')}\n"
                    f"• Razón: Cancelación por el solicitante\n"
                    f"• Acción realizada por: {solicitud.solicitante.get_full_name() or 'Sistema'}"
                )
            else:  # pendiente
                accion = 'creacion'
                detalles = (
                    f"NUEVA SOLICITUD DE INTERCAMBIO\n"
                    f"• Solicitante: {solicitud.solicitante.get_full_name() or solicitud.solicitante.email}\n"
                    f"• Receptor: {solicitud.receptor.get_full_name() or solicitud.receptor.email}\n"
                    f"• Oportunidad Origen: {solicitud.oportunidad_origen.titulo}\n"
                    f"• Oportunidad Destino: {solicitud.oportunidad_destino.titulo}\n"
                    f"• Mensaje: {solicitud.mensaje or 'Sin mensaje'}\n"
                    f"• Fecha: {timezone.localtime(solicitud.fecha_creacion).strftime('%d/%m/%Y %H:%M')}\n"
                    f"• Estado: Pendiente de revisión"
                )
            
            # Buscar si ya existe un registro de historial para esta acción
            historial_existente = solicitud.historial.filter(accion=accion).first()
            
            if historial_existente and not force_update:
                self.stdout.write(self.style.SUCCESS(f'El historial para la solicitud {solicitud.id} ya existe (estado: {solicitud.estado})'))
                continue
                
            # Crear o actualizar el registro de historial
            fecha_accion = timezone.localtime(solicitud.fecha_actualizacion if accion != 'creacion' else solicitud.fecha_creacion)
            
            if historial_existente and force_update:
                # Actualizar el registro existente
                historial_existente.detalles = detalles
                historial_existente.fecha = fecha_accion
                historial_existente.save()
                self.stdout.write(self.style.SUCCESS(f'Actualizado historial para solicitud {solicitud.id} (estado: {solicitud.estado})'))
            else:
                # Crear un nuevo registro de historial
                HistorialPermutacion.objects.create(
                    solicitud=solicitud,
                    accion=accion,
                    detalles=detalles,
                    fecha=fecha_accion,
                    usuario=solicitud.solicitante  # Asumimos que el solicitante realizó la acción
                )
                self.stdout.write(self.style.SUCCESS(f'Creado historial para solicitud {solicitud.id} (estado: {solicitud.estado})'))
        
        self.stdout.write(self.style.SUCCESS('Proceso de actualización de historial completado'))
