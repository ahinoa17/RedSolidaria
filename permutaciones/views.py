# permutaciones/views.py
from django.core.exceptions import ValidationError
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction, models
from django.views.generic import ListView, DetailView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils import timezone

from .models import SolicitudPermutacion
from inscripciones.models import Inscripcion
from oportunidades.models import OportunidadVoluntariado

class ListaPermutacionesView(LoginRequiredMixin, ListView):
    model = SolicitudPermutacion
    template_name = 'permutaciones/lista.html'
    context_object_name = 'solicitudes'
    
    def get_queryset(self):
        # Obtener las solicitudes enviadas y recibidas por el usuario
        return SolicitudPermutacion.objects.filter(
            models.Q(solicitante=self.request.user) | 
            models.Q(receptor=self.request.user)
        ).select_related('oportunidad_origen', 'oportunidad_destino', 'solicitante', 'receptor')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        # Obtener las inscripciones del usuario para mostrar en el formulario
        context['mis_inscripciones'] = Inscripcion.objects.filter(
            usuario=user,
            estado='aceptada',
            oportunidad__fecha_fin__gte=timezone.now().date()
        ).select_related('oportunidad')
        
        # Separar solicitudes enviadas y recibidas
        context['solicitudes_enviadas'] = [s for s in context['solicitudes'] if s.solicitante == user]
        context['solicitudes_recibidas'] = [s for s in context['solicitudes'] if s.receptor == user]
        
        # Obtener oportunidades disponibles para permutar
        oportunidad_id = self.request.GET.get('oportunidad_id')
        if oportunidad_id:
            try:
                # Verificar que el usuario esté inscrito en la oportunidad seleccionada
                inscripcion = Inscripcion.objects.get(
                    oportunidad_id=oportunidad_id,
                    usuario=user,
                    estado='aceptada'
                )
                
                oportunidad_actual = inscripcion.oportunidad
                context['oportunidad_actual'] = oportunidad_actual
                
                # Obtener oportunidades con las que se puede intercambiar
                oportunidades_permutables = SolicitudPermutacion.calcular_permutaciones_posibles(
                    user, 
                    oportunidad_actual
                )
                
                # Excluir oportunidades que ya tienen solicitudes pendientes
                oportunidades_con_solicitud = SolicitudPermutacion.objects.filter(
                    models.Q(solicitante=user, oportunidad_origen=oportunidad_actual) |
                    models.Q(receptor=user, oportunidad_destino=oportunidad_actual),
                    estado='pendiente'
                ).values_list('oportunidad_destino_id', flat=True)
                
                oportunidades_permutables = oportunidades_permutables.exclude(
                    id__in=oportunidades_con_solicitud
                )
                
                context['oportunidades_permutables'] = oportunidades_permutables
                
            except (OportunidadVoluntariado.DoesNotExist, Inscripcion.DoesNotExist):
                messages.error(self.request, 'No tienes permiso para intercambiar esta oportunidad')
        
        return context

@login_required
def crear_solicitud(request, oportunidad_id):
    """
    Vista para crear una nueva solicitud de permutación.
    """
    oportunidad_origen = get_object_or_404(OportunidadVoluntariado, id=oportunidad_id)
    
    # Verificar que el usuario está inscrito en la oportunidad de origen
    try:
        inscripcion_origen = Inscripcion.objects.get(
            usuario=request.user,
            oportunidad=oportunidad_origen,
            estado='aceptada'
        )
    except Inscripcion.DoesNotExist:
        messages.error(request, 'No estás inscrito en esta oportunidad o no está aceptada')
        return redirect('permutaciones:lista')
    
    if request.method == 'POST':
        oportunidad_destino_id = request.POST.get('oportunidad_destino')
        mensaje = request.POST.get('mensaje', 'Solicitud de intercambio de turno')
        
        try:
            # Validar que la oportunidad de destino existe
            oportunidad_destino = OportunidadVoluntariado.objects.get(id=oportunidad_destino_id)
            
            # Obtener un usuario inscrito en la oportunidad de destino
            inscripcion_destino = Inscripcion.objects.filter(
                oportunidad=oportunidad_destino,
                estado='aceptada'
            ).exclude(
                usuario=request.user
            ).first()
            
            if not inscripcion_destino:
                messages.error(request, 'No hay usuarios disponibles para intercambiar en esta oportunidad')
                return redirect('permutaciones:lista')
            
            # Crear la solicitud de permutación
            solicitud = SolicitudPermutacion(
                solicitante=request.user,
                receptor=inscripcion_destino.usuario,
                oportunidad_origen=oportunidad_origen,
                oportunidad_destino=oportunidad_destino,
                mensaje=mensaje
            )
            
            # Validar la solicitud
            solicitud.full_clean()
            
            # Guardar la solicitud
            solicitud.save()
            
            messages.success(request, 'Solicitud de permutación enviada correctamente')
            return redirect('permutaciones:lista')
            
        except OportunidadVoluntariado.DoesNotExist:
            messages.error(request, 'La oportunidad de destino no existe')
        except ValidationError as e:
            messages.error(request, f'Error al crear la solicitud: {e}')
        except Exception as e:
            messages.error(request, f'Error inesperado: {str(e)}')
    
    # Redirigir a la lista de permutaciones
    return redirect('permutaciones:lista')

@login_required
def aceptar_solicitud(request, pk):
    """
    Vista para aceptar una solicitud de permutación.
    """
    if request.method != 'POST':
        return redirect('permutaciones:lista')
        
    try:
        solicitud = SolicitudPermutacion.objects.get(pk=pk, receptor=request.user, estado='pendiente')
    except SolicitudPermutacion.DoesNotExist:
        messages.error(request, 'La solicitud no existe o ya ha sido procesada.')
        return redirect('permutaciones:lista')
    
    # Aceptar la solicitud (esto ejecutará la lógica de intercambio)
    resultado, mensaje = solicitud.aceptar()
    
    # Mostrar el mensaje solo una vez
    if resultado == 'aceptada':
        messages.success(request, mensaje)
    elif resultado == 'rechazada':
        messages.warning(request, mensaje)
    else:  # error
        messages.error(request, mensaje)
    
    return redirect('permutaciones:lista')

@login_required
def rechazar_solicitud(request, pk):
    """
    Vista para rechazar una solicitud de permutación.
    """
    solicitud = get_object_or_404(
        SolicitudPermutacion, 
        pk=pk, 
        receptor=request.user,
        estado='pendiente'
    )
    
    if request.method == 'POST':
        try:
            solicitud.rechazar()
            messages.success(request, 'Has rechazado la solicitud de permutación')
        except ValidationError as e:
            messages.error(request, f'Error al rechazar la solicitud: {e}')
    
    return redirect('permutaciones:lista')

@login_required
def cancelar_solicitud(request, pk):
    """
    Vista para cancelar una solicitud de permutación.
    """
    solicitud = get_object_or_404(SolicitudPermutacion, pk=pk, solicitante=request.user)
    
    if request.method == 'POST':
        try:
            solicitud.cancelar()
            messages.success(request, 'La solicitud de permutación ha sido cancelada.')
        except ValidationError as e:
            messages.error(request, str(e))
    
    return redirect('permutaciones:lista')

class DetalleSolicitudView(LoginRequiredMixin, DetailView):
    """
    Vista para mostrar los detalles de una solicitud de permutación.
    """
    model = SolicitudPermutacion
    template_name = 'permutaciones/detalle_solicitud.html'
    context_object_name = 'solicitud'
    
    def get_queryset(self):
        # Solo permitir ver las solicitudes donde el usuario es el solicitante o el receptor
        return SolicitudPermutacion.objects.filter(
            models.Q(solicitante=self.request.user) | 
            models.Q(receptor=self.request.user)
        ).select_related('oportunidad_origen', 'oportunidad_destino', 'solicitante', 'receptor')