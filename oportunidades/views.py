from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import OportunidadVoluntariado
from .forms import OportunidadVoluntariadoForm

def superusuario_requerido(user):
    return user.is_superuser

def lista_oportunidades(request):
    oportunidades = OportunidadVoluntariado.objects.all()
    
    # Obtener las IDs de las oportunidades en las que el usuario está inscrito
    if request.user.is_authenticated and not request.user.is_superuser:
        inscripciones_usuario = list(request.user.inscripcion_set.select_related('oportunidad').values_list('oportunidad_id', flat=True))
    else:
        inscripciones_usuario = []
    
    return render(request, 'oportunidades/lista.html', {
        'oportunidades': oportunidades,
        'inscripciones_usuario': inscripciones_usuario
    })

def detalle_oportunidad(request, pk):
    oportunidad = get_object_or_404(OportunidadVoluntariado, pk=pk)
    
    # Verificar si el usuario está inscrito en esta oportunidad
    esta_inscrito = False
    if request.user.is_authenticated and not request.user.is_superuser:
        esta_inscrito = request.user.inscripcion_set.filter(oportunidad=oportunidad).exists()
    
    return render(request, 'oportunidades/detalle.html', {
        'oportunidad': oportunidad,
        'esta_inscrito': esta_inscrito
    })

@login_required
@user_passes_test(superusuario_requerido, login_url='lista_oportunidades')
def crear_oportunidad(request):
    if request.method == 'POST':
        form = OportunidadVoluntariadoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_oportunidades')
    else:
        form = OportunidadVoluntariadoForm()
    return render(request, 'oportunidades/form.html', {'form': form})

@login_required
@user_passes_test(superusuario_requerido, login_url='lista_oportunidades')
def editar_oportunidad(request, pk):
    oportunidad = get_object_or_404(OportunidadVoluntariado, pk=pk)
    if request.method == 'POST':
        form = OportunidadVoluntariadoForm(request.POST, instance=oportunidad)
        if form.is_valid():
            form.save()
            return redirect('detalle_oportunidad', pk=pk)
    else:
        form = OportunidadVoluntariadoForm(instance=oportunidad)
    return render(request, 'oportunidades/form.html', {'form': form})

@login_required
@user_passes_test(superusuario_requerido, login_url='lista_oportunidades')
def eliminar_oportunidad(request, pk):
    oportunidad = get_object_or_404(OportunidadVoluntariado, pk=pk)
    if request.method == 'POST':
        oportunidad.delete()
        return redirect('lista_oportunidades')
    return render(request, 'oportunidades/confirmar_eliminar.html', {'oportunidad': oportunidad})