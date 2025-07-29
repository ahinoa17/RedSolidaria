from django.shortcuts import render, get_object_or_404, redirect
from .models import PermutacionParticipantes
from .forms import PermutacionParticipantesForm
from django.contrib.auth.decorators import login_required

@login_required
def lista_permutaciones(request):
    permutaciones = PermutacionParticipantes.objects.all()
    return render(request, 'permutaciones/lista.html', {'permutaciones': permutaciones})

@login_required
def crear_permutacion(request):
    if request.method == 'POST':
        form = PermutacionParticipantesForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_permutaciones')
    else:
        form = PermutacionParticipantesForm()
    return render(request, 'permutaciones/form.html', {'form': form})

@login_required
def editar_permutacion(request, pk):
    permutacion = get_object_or_404(PermutacionParticipantes, pk=pk)
    if request.method == 'POST':
        form = PermutacionParticipantesForm(request.POST, instance=permutacion)
        if form.is_valid():
            form.save()
            return redirect('lista_permutaciones')
    else:
        form = PermutacionParticipantesForm(instance=permutacion)
    return render(request, 'permutaciones/form.html', {'form': form})

@login_required
def eliminar_permutacion(request, pk):
    permutacion = get_object_or_404(PermutacionParticipantes, pk=pk)
    if request.method == 'POST':
        permutacion.delete()
        return redirect('lista_permutaciones')
    return render(request, 'permutaciones/confirmar_eliminar.html', {'permutacion': permutacion})
