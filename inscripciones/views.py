from django.shortcuts import render, get_object_or_404, redirect
from .models import Inscripcion
from .forms import InscripcionForm
from django.contrib.auth.decorators import login_required

@login_required
def mis_inscripciones(request):
    inscripciones = Inscripcion.objects.filter(usuario=request.user)
    return render(request, 'inscripciones/mis_inscripciones.html', {'inscripciones': inscripciones})

@login_required
def crear_inscripcion(request):
    if request.method == 'POST':
        form = InscripcionForm(request.POST)
        if form.is_valid():
            inscripcion = form.save(commit=False)
            inscripcion.usuario = request.user
            inscripcion.save()
            return redirect('mis_inscripciones')
    else:
        form = InscripcionForm()
    return render(request, 'inscripciones/form.html', {'form': form})

@login_required
def editar_inscripcion(request, pk):
    inscripcion = get_object_or_404(Inscripcion, pk=pk, usuario=request.user)
    if request.method == 'POST':
        form = InscripcionForm(request.POST, instance=inscripcion)
        if form.is_valid():
            form.save()
            return redirect('mis_inscripciones')
    else:
        form = InscripcionForm(instance=inscripcion)
    return render(request, 'inscripciones/form.html', {'form': form})

@login_required
def eliminar_inscripcion(request, pk):
    inscripcion = get_object_or_404(Inscripcion, pk=pk, usuario=request.user)
    if request.method == 'POST':
        inscripcion.delete()
        return redirect('mis_inscripciones')
    return render(request, 'inscripciones/confirmar_eliminar.html', {'inscripcion': inscripcion})