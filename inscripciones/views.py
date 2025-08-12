from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, CreateView, DeleteView
from django.urls import reverse_lazy
from .models import Inscripcion
from oportunidades.models import OportunidadVoluntariado

class MisInscripcionesView(LoginRequiredMixin, ListView):
    model = Inscripcion
    template_name = 'inscripciones/mis_inscripciones.html'
    context_object_name = 'inscripciones'

    def get_queryset(self):
        return Inscripcion.objects.filter(usuario=self.request.user)


class GestionInscripcionesView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Inscripcion
    template_name = 'inscripciones/gestion_inscripciones.html'
    context_object_name = 'inscripciones'
    
    def test_func(self):
        return self.request.user.is_superuser
        
    def get_queryset(self):
        # Mostrar solo inscripciones pendientes
        return Inscripcion.objects.filter(estado='pendiente').select_related('usuario', 'oportunidad')


@login_required
@user_passes_test(lambda u: u.is_superuser)
def aceptar_inscripcion(request, pk):
    inscripcion = get_object_or_404(Inscripcion, pk=pk)
    if request.method == 'POST':
        inscripcion.estado = 'aceptada'
        inscripcion.save()
        messages.success(request, f'Inscripción de {inscripcion.usuario.get_full_name()} aceptada correctamente.')
    return redirect('inscripciones:gestion_inscripciones')


@login_required
@user_passes_test(lambda u: u.is_superuser)
def rechazar_inscripcion(request, pk):
    inscripcion = get_object_or_404(Inscripcion, pk=pk)
    if request.method == 'POST':
        inscripcion.estado = 'rechazada'
        inscripcion.save()
        messages.warning(request, f'Inscripción de {inscripcion.usuario.get_full_name()} rechazada.')
    return redirect('inscripciones:gestion_inscripciones')

@login_required
def inscribirse_oportunidad(request, oportunidad_id):
    oportunidad = get_object_or_404(OportunidadVoluntariado, id=oportunidad_id)
    
    # Verificar si el usuario ya está inscrito
    if Inscripcion.objects.filter(usuario=request.user, oportunidad=oportunidad).exists():
        messages.warning(request, 'Ya estás inscrito en esta oportunidad.')
        return redirect('detalle_oportunidad', pk=oportunidad_id)
    
    if request.method == 'POST':
        try:
            Inscripcion.objects.create(
                usuario=request.user,
                oportunidad=oportunidad,
                estado='pendiente'
            )
            messages.success(request, '¡Te has inscrito correctamente en la oportunidad!')
            return redirect('mis_inscripciones')
        except Exception as e:
            messages.error(request, 'Ocurrió un error al procesar tu inscripción.')
            return redirect('detalle_oportunidad', pk=oportunidad_id)
            
    return render(request, 'inscripciones/confirmar_inscripcion.html', {
        'oportunidad': oportunidad
    })

@login_required
def eliminar_inscripcion(request, pk):
    try:
        inscripcion = Inscripcion.objects.get(pk=pk, usuario=request.user)
        
        if request.method == 'POST':
            # Obtener el título de la oportunidad antes de eliminar para el mensaje
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