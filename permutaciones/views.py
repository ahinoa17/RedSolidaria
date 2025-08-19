# permutaciones/views.py
# Importaciones de Django y utilidades estándar
from django.core.exceptions import ValidationError  # Para manejo de validaciones
from django.shortcuts import render, get_object_or_404, redirect  # Utilidades para vistas basadas en funciones
from django.contrib.auth.decorators import login_required  # Decorador para requerir autenticación
from django.contrib import messages  # Sistema de mensajes para el usuario
from django.db import transaction, models  # Utilidades de base de datos
from django.views.generic import ListView, DetailView, TemplateView  # Vistas genéricas basadas en clases
from django.contrib.auth.mixins import LoginRequiredMixin  # Mixin para requerir autenticación en VBC
from django.urls import reverse_lazy  # Para URLs con evaluación perezosa
from django.utils import timezone  # Manejo de zonas horarias
from django.contrib.auth import get_user_model  # Obtener el modelo de usuario activo

# Importaciones de modelos locales
from .models import SolicitudPermutacion, HistorialPermutacion  # Modelos de la aplicación
from inscripciones.models import Inscripcion  # Modelo de inscripciones
from oportunidades.models import OportunidadVoluntariado  # Modelo de oportunidades de voluntariado

class ListaPermutacionesView(LoginRequiredMixin, ListView):
    """
    Vista basada en clase para mostrar la lista de solicitudes de permutación.
    Hereda de LoginRequiredMixin para requerir autenticación y ListView para funcionalidad de lista.
    """
    model = SolicitudPermutacion  # Modelo principal para la vista
    template_name = 'permutaciones/lista.html'  # Plantilla para renderizar
    context_object_name = 'solicitudes'  # Nombre de la variable en el contexto de la plantilla
    
    def get_queryset(self):
        """
        Obtiene el conjunto de consultas para las solicitudes de permutación.
        Filtra para mostrar solo las solicitudes donde el usuario actual es el solicitante o el receptor.
        Optimiza las consultas relacionadas con select_related.
        """
        return SolicitudPermutacion.objects.filter(
            models.Q(solicitante=self.request.user) |  # Usuario es quien envía
            models.Q(receptor=self.request.user)       # O usuario es quien recibe
        ).select_related(
            'oportunidad_origen',  # Optimización para evitar consultas N+1
            'oportunidad_destino',
            'solicitante',
            'receptor'
        )
    
    def get_context_data(self, **kwargs):
        """
        Añade datos adicionales al contexto de la plantilla.
        Incluye inscripciones del usuario, solicitudes enviadas/recibidas y oportunidades para permutar.
        """
        # Obtener el contexto base de la clase padre
        context = super().get_context_data(**kwargs)
        # Referencia al usuario actual para uso posterior
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
                
                # Usar el método mejorado del modelo para obtener oportunidades con usuarios disponibles
                oportunidades_permutables = SolicitudPermutacion.calcular_permutaciones_posibles(
                    user, oportunidad_actual
                )
                
                # Verificar solicitudes pendientes existentes para cada oportunidad
                for op in oportunidades_permutables:
                    op['tiene_solicitud_pendiente'] = SolicitudPermutacion.objects.filter(
                        solicitante=user,
                        oportunidad_origen=oportunidad_actual,
                        oportunidad_destino_id=op['oportunidad']['id'],
                        estado='pendiente'
                    ).exists()
                
                context['oportunidades_permutables'] = oportunidades_permutables
                
            except (OportunidadVoluntariado.DoesNotExist, Inscripcion.DoesNotExist):
                messages.error(self.request, 'No tienes permiso para intercambiar esta oportunidad')
        
        return context
        
    def obtener_usuarios_disponibles_para_intercambio(self, usuario, oportunidad_origen, oportunidad_destino):
        """
        Obtiene los usuarios con los que se puede hacer intercambio para una oportunidad específica.
        """
        # 1. Usuarios que están inscritos en la oportunidad destino
        usuarios_en_destino = Inscripcion.objects.filter(
            oportunidad=oportunidad_destino,
            estado='aceptada'
        ).exclude(usuario=usuario)  # Excluir al usuario actual
        
        # 2. Filtrar usuarios que no estén ya en la oportunidad de origen
        #    y que no tengan conflictos de horario
        usuarios_disponibles = get_user_model().objects.none()
        
        for inscripcion in usuarios_en_destino.select_related('usuario'):
            usuario_destino = inscripcion.usuario
            
            # Verificar que el usuario no esté ya en la oportunidad de origen
            if not Inscripcion.objects.filter(
                usuario=usuario_destino,
                oportunidad=oportunidad_origen
            ).exists():
                # Verificar que no haya conflictos de horario
                if not self.tiene_conflicto_horario(usuario_destino, oportunidad_origen):
                    usuarios_disponibles |= get_user_model().objects.filter(id=usuario_destino.id)
        
        return usuarios_disponibles
    
    def tiene_conflicto_horario(self, usuario, oportunidad):
        """
        Verifica si el usuario ya tiene una actividad en el mismo horario.
        """
        # Obtener todas las inscripciones activas del usuario
        inscripciones = Inscripcion.objects.filter(
            usuario=usuario,
            estado='aceptada',
            oportunidad__fecha_fin__gte=timezone.now().date()
        ).exclude(oportunidad=oportunidad).select_related('oportunidad')
        
        # Verificar conflictos de horario
        for inscripcion in inscripciones:
            if self.horarios_se_superponen(inscripcion.oportunidad, oportunidad):
                return True
        
        return False
    
    def horarios_se_superponen(self, op1, op2):
        """
        Verifica si dos oportunidades tienen horarios que se superponen.
        Como no tenemos campos separados para día y hora, asumimos que si tienen el mismo horario,
        hay superposición. Esto es una simplificación.
        """
        # Si los horarios son iguales, hay superposición
        return op1.horario == op2.horario

@login_required  # Requiere que el usuario esté autenticado
def crear_solicitud(request, oportunidad_id):
    """
    Vista basada en función para crear una nueva solicitud de permutación.
    
    Args:
        request: Objeto HttpRequest
        oportunidad_id: ID de la oportunidad de origen para el intercambio
        
    Returns:
        HttpResponse: Redirección a la lista de permutaciones con mensaje de estado
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
        usuario_destino_id = request.POST.get('usuario_destino')
        mensaje = request.POST.get('mensaje', 'Solicitud de intercambio de turno')
        
        try:
            # Validar que la oportunidad de destino existe
            oportunidad_destino = OportunidadVoluntariado.objects.get(id=oportunidad_destino_id)
            usuario_destino = get_user_model().objects.get(id=usuario_destino_id)
            
            # Verificar que el usuario destino esté inscrito en la oportunidad destino
            if not Inscripcion.objects.filter(
                usuario=usuario_destino,
                oportunidad=oportunidad_destino,
                estado='aceptada'
            ).exists():
                messages.error(request, 'El usuario seleccionado ya no está disponible para intercambio')
                return redirect('permutaciones:lista')
            
            # Verificar que no exista ya una solicitud similar
            if SolicitudPermutacion.objects.filter(
                solicitante=request.user,
                receptor=usuario_destino,
                oportunidad_origen=oportunidad_origen,
                oportunidad_destino=oportunidad_destino,
                estado='pendiente'
            ).exists():
                messages.warning(request, 'Ya existe una solicitud pendiente para este intercambio')
                return redirect('permutaciones:lista')
            
            # Crear la solicitud
            solicitud = SolicitudPermutacion(
                solicitante=request.user,
                receptor=usuario_destino,
                oportunidad_origen=oportunidad_origen,
                oportunidad_destino=oportunidad_destino,
                mensaje=mensaje
            )
            
            # Establecer el usuario actual para el historial
            solicitud._usuario_actual = request.user
            
            # Validar y guardar la solicitud
            solicitud.full_clean()
            solicitud.save()
            
            messages.success(request, 'Solicitud de intercambio enviada correctamente')
            return redirect('permutaciones:lista')
            
        except (OportunidadVoluntariado.DoesNotExist, get_user_model().DoesNotExist):
            messages.error(request, 'Error al procesar la solicitud. Por favor, inténtalo de nuevo.')
        except ValidationError as e:
            messages.error(request, f'Error de validación: {e}')
        except Exception as e:
            messages.error(request, f'Error inesperado: {str(e)}')
    
    # Redirigir a la lista de permutaciones
    return redirect('permutaciones:lista')

@login_required  # Requiere que el usuario esté autenticado
def aceptar_solicitud(request, pk):
    """
    Vista para procesar la aceptación de una solicitud de permutación.
    
    Args:
        request: Objeto HttpRequest (debe ser POST)
        pk: ID de la solicitud de permutación
        
    Returns:
        HttpResponse: Redirección a la lista de permutaciones con mensaje de estado
    """
    if request.method != 'POST':
        messages.error(request, 'Método no permitido')
        return redirect('permutaciones:lista')
        
    try:
        solicitud = SolicitudPermutacion.objects.get(pk=pk, receptor=request.user, estado='pendiente')
    except SolicitudPermutacion.DoesNotExist:
        messages.error(request, 'La solicitud no existe o ya ha sido procesada.')
        return redirect('permutaciones:lista')
    
    try:
        # Establecer el usuario actual para el historial
        solicitud._usuario_actual = request.user
        # Aceptar la solicitud
        resultado, mensaje = solicitud.aceptar()
        
        # Mostrar el mensaje solo una vez
        if resultado == 'aceptada':
            messages.success(request, mensaje)
        elif resultado == 'rechazada':
            messages.warning(request, mensaje)
        else:  # error
            messages.error(request, mensaje)
        
        return redirect('permutaciones:lista')
    except ValidationError as e:
        messages.error(request, f'Error al aceptar la solicitud: {e}')
    except Exception as e:
        messages.error(request, f'Error inesperado: {str(e)}')

@login_required  # Requiere que el usuario esté autenticado
def rechazar_solicitud(request, pk):
    """
    Vista para procesar el rechazo de una solicitud de permutación.
    
    Args:
        request: Objeto HttpRequest (debe ser POST)
        pk: ID de la solicitud de permutación a rechazar
        
    Returns:
        HttpResponse: Redirección a la lista de permutaciones con mensaje de estado
    """
    if request.method != 'POST':
        messages.error(request, 'Método no permitido')
        return redirect('permutaciones:lista')
    
    solicitud = get_object_or_404(SolicitudPermutacion, id=pk, receptor=request.user, estado='pendiente')
    
    try:
        # Establecer el usuario actual para el historial
        solicitud._usuario_actual = request.user
        # Rechazar la solicitud
        solicitud.rechazar()
        messages.success(request, 'Has rechazado la solicitud de permutación')
    except ValidationError as e:
        messages.error(request, f'Error al rechazar la solicitud: {e}')
    
    return redirect('permutaciones:lista')

@login_required  # Requiere que el usuario esté autenticado
def cancelar_solicitud(request, pk):
    """
    Vista para cancelar una solicitud de permutación existente.
    Solo el solicitante original puede cancelar la solicitud.
    
    Args:
        request: Objeto HttpRequest (debe ser POST)
        pk: ID de la solicitud de permutación a cancelar
        
    Returns:
        HttpResponse: Redirección a la lista de permutaciones con mensaje de estado
    """
    if request.method != 'POST':
        messages.error(request, 'Método no permitido')
        return redirect('permutaciones:lista')
    
    solicitud = get_object_or_404(SolicitudPermutacion, id=pk, solicitante=request.user, estado='pendiente')
    
    try:
        # Establecer el usuario actual para el historial
        solicitud._usuario_actual = request.user
        # Cancelar la solicitud
        solicitud.estado = 'cancelada'
        solicitud.fecha_actualizacion = timezone.now()
        
        # Registrar la cancelación en el historial
        HistorialPermutacion.objects.create(
            solicitud=solicitud,
            accion='cancelacion',
            detalles='Solicitud de intercambio cancelada por el solicitante',
            usuario=request.user
        )
        
        solicitud.save()
        messages.success(request, 'La solicitud de permutación ha sido cancelada.')
    except ValidationError as e:
        messages.error(request, str(e))
    
    return redirect('permutaciones:lista')

class DetalleSolicitudView(LoginRequiredMixin, DetailView):
    """
    Vista basada en clase para mostrar los detalles de una solicitud de permutación.
    
    Atributos:
        model: Modelo principal de la vista (SolicitudPermutacion)
        template_name: Ruta a la plantilla para renderizar
        context_object_name: Nombre de la variable en el contexto de la plantilla
    """
    model = SolicitudPermutacion  # Modelo asociado a la vista
    template_name = 'permutaciones/detalle_solicitud.html'  # Plantilla a utilizar
    context_object_name = 'solicitud'  # Nombre del objeto en el contexto
    
    def get_queryset(self):
        """
        Filtra las solicitudes para mostrar solo aquellas donde el usuario actual
        es el solicitante o el receptor.
        
        Returns:
            QuerySet: Conjunto de solicitudes filtradas con relaciones optimizadas
        """
        return SolicitudPermutacion.objects.filter(
            models.Q(solicitante=self.request.user) |  # Usuario es quien envía
            models.Q(receptor=self.request.user)       # O usuario es quien recibe
        ).select_related(  # Optimización para evitar consultas N+1
            'oportunidad_origen',
            'oportunidad_destino',
            'solicitante',
            'receptor'
        )