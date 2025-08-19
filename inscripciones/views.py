# Importaciones de Django y utilidades
from django.contrib import messages  # Para mensajes al usuario
from django.contrib.auth.decorators import login_required, user_passes_test  # Para control de acceso
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin  # Mixins para vistas basadas en clases
from django.shortcuts import render, get_object_or_404, redirect  # Funciones de utilidad para vistas
from django.views.generic import ListView, CreateView, DeleteView  # Vistas genéricas
from django.urls import reverse_lazy  # Para URLs con evaluación perezosa

# Importación de modelos
from .models import Inscripcion
from oportunidades.models import OportunidadVoluntariado
from permutaciones.models import HistorialPermutacion


class MisInscripcionesView(LoginRequiredMixin, ListView):
    """Vista para mostrar las inscripciones del usuario actual."""
    model = Inscripcion
    template_name = 'inscripciones/mis_inscripciones.html'
    context_object_name = 'inscripciones'

    def get_queryset(self):
        """Retorna solo las inscripciones del usuario actual."""
        return Inscripcion.objects.filter(usuario=self.request.user)


class GestionInscripcionesView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    """Vista para que los administradores gestionen todas las inscripciones."""
    model = Inscripcion
    template_name = 'inscripciones/gestion_inscripciones.html'
    context_object_name = 'inscripciones'
    
    def test_func(self):
        """Permite el acceso a superusuarios y administradores."""
        return self.request.user.is_superuser or getattr(self.request.user, 'acceso_admin', False)
        
    def get_queryset(self):
        """Filtra las inscripciones según el estado seleccionado."""
        estado = self.request.GET.get('estado', 'pendiente')
        
        # Si es la pestaña de historial, no necesitamos las inscripciones
        if estado == 'historial':
            return Inscripcion.objects.none()
            
        queryset = Inscripcion.objects.all()
        
        if estado != 'todas':
            queryset = queryset.filter(estado=estado)
            
        return queryset.select_related('usuario', 'oportunidad', 'oportunidad__organizacion')
    
    def get_context_data(self, **kwargs):
        """Agrega contadores, estado actual y datos de historial al contexto."""
        context = super().get_context_data(**kwargs)
        estado_actual = self.request.GET.get('estado', 'pendiente')
        
        # Contadores para las pestañas
        context['contadores'] = {
            'pendiente': Inscripcion.objects.filter(estado='pendiente').count(),
            'aceptada': Inscripcion.objects.filter(estado='aceptada').count(),
            'rechazada': Inscripcion.objects.filter(estado='rechazada').count(),
            'historial': HistorialPermutacion.objects.count(),
            'total': Inscripcion.objects.count()
        }
        
        # Si es la pestaña de historial, obtenemos los registros
        if estado_actual == 'historial':
            context['historial_intercambios'] = HistorialPermutacion.objects.select_related(
                'solicitud', 'solicitud__solicitante', 'solicitud__receptor',
                'solicitud__oportunidad_origen', 'solicitud__oportunidad_destino',
                'usuario'
            ).order_by('-fecha')
        
        context['estado_actual'] = estado_actual
        
        # Títulos según la pestaña activa
        titulos = {
            'pendiente': 'Inscripciones Pendientes',
            'aceptada': 'Inscripciones Aceptadas',
            'rechazada': 'Inscripciones Rechazadas',
            'historial': 'Historial de Intercambios',
            'todas': 'Todas las Inscripciones'
        }
        
        context['titulo_estado'] = titulos.get(estado_actual, 'Inscripciones')
        
        return context


@login_required
@user_passes_test(lambda u: u.is_superuser or getattr(u, 'acceso_admin', False))
def aceptar_inscripcion(request, pk):
    """Vista para que un administrador acepte una inscripción."""
    inscripcion = get_object_or_404(Inscripcion, pk=pk)
    if request.method == 'POST':
        inscripcion.estado = 'aceptada'
        inscripcion.save()
        messages.success(request, f'Inscripción de {inscripcion.usuario.get_full_name()} aceptada correctamente.')
    return redirect('inscripciones:gestion_inscripciones')


@login_required
@user_passes_test(lambda u: u.is_superuser or getattr(u, 'acceso_admin', False))
def rechazar_inscripcion(request, pk):
    """Vista para que un administrador rechace una inscripción."""
    inscripcion = get_object_or_404(Inscripcion, pk=pk)
    if request.method == 'POST':
        inscripcion.estado = 'rechazada'
        inscripcion.save()
        messages.warning(request, f'Inscripción de {inscripcion.usuario.get_full_name()} rechazada.')
    return redirect('inscripciones:gestion_inscripciones')


@login_required
def inscribirse_oportunidad(request, oportunidad_id):
    """Vista para que un usuario se inscriba a una oportunidad."""
    oportunidad = get_object_or_404(OportunidadVoluntariado, id=oportunidad_id)
    
    # Validaciones previas
    if Inscripcion.objects.filter(usuario=request.user, oportunidad=oportunidad).exists():
        messages.warning(request, 'Ya estás inscrito en esta oportunidad.')
        return redirect('detalle_oportunidad', pk=oportunidad_id)
    
    if oportunidad.cupos <= 0:
        messages.error(request, 'Lo sentimos, no hay cupos disponibles para esta oportunidad.')
        return redirect('detalle_oportunidad', pk=oportunidad_id)
    
    if oportunidad.estado != 'abierta':
        messages.error(request, 'Esta oportunidad ya no está disponible para inscripciones.')
        return redirect('detalle_oportunidad', pk=oportunidad_id)
    
    if request.method == 'POST':
        try:
            if oportunidad.cupos <= 0:
                messages.error(request, 'Lo sentimos, los cupos para esta oportunidad se han agotado.')
                return redirect('detalle_oportunidad', pk=oportunidad_id)
                
            # Crear la inscripción
            Inscripcion.objects.create(
                usuario=request.user,
                oportunidad=oportunidad,
                estado='pendiente'
            )
            
            # Actualizar cupos
            oportunidad.cupos -= 1
            if oportunidad.cupos <= 0:
                oportunidad.estado = 'cerrada'
            oportunidad.save()
            
            messages.success(request, '¡Te has inscrito correctamente en la oportunidad!')
            return redirect('inscripciones:mis_inscripciones')
            
        except Exception as e:
            messages.error(request, f'Ocurrió un error al procesar tu inscripción: {str(e)}')
            return redirect('detalle_oportunidad', pk=oportunidad_id)
            
    return render(request, 'inscripciones/confirmar_inscripcion.html', {
        'oportunidad': oportunidad,
        'cupos_disponibles': oportunidad.cupos > 0
    })


@login_required
def eliminar_inscripcion(request, pk):
    """Vista para que un usuario cancele su propia inscripción."""
    try:
        inscripcion = Inscripcion.objects.get(pk=pk, usuario=request.user)
        
        if request.method == 'POST':
            titulo_oportunidad = str(inscripcion.oportunidad)
            inscripcion.delete()
            messages.success(request, f'Has cancelado tu inscripción en: {titulo_oportunidad}')
            return redirect('inscripciones:mis_inscripciones')
            
        return render(request, 'inscripciones/confirmar_eliminacion.html', {
            'inscripcion': inscripcion
        })
        
    except Inscripcion.DoesNotExist:
        messages.error(request, 'La inscripción que intentas cancelar no existe o no tienes permiso para hacerlo.')
        return redirect('inscripciones:mis_inscripciones')