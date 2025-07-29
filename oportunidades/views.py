from django.shortcuts import render, get_object_or_404, redirect
from .models import OportunidadVoluntariado
from .forms import OportunidadVoluntariadoForm

def lista_oportunidades(request):
    oportunidades = OportunidadVoluntariado.objects.all()
    return render(request, 'oportunidades/lista.html', {'oportunidades': oportunidades})

def detalle_oportunidad(request, pk):
    oportunidad = get_object_or_404(OportunidadVoluntariado, pk=pk)
    return render(request, 'oportunidades/detalle.html', {'oportunidad': oportunidad})

def crear_oportunidad(request):
    if request.method == 'POST':
        form = OportunidadVoluntariadoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_oportunidades')
    else:
        form = OportunidadVoluntariadoForm()
    return render(request, 'oportunidades/form.html', {'form': form})

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

def eliminar_oportunidad(request, pk):
    oportunidad = get_object_or_404(OportunidadVoluntariado, pk=pk)
    if request.method == 'POST':
        oportunidad.delete()
        return redirect('lista_oportunidades')
    return render(request, 'oportunidades/confirmar_eliminar.html', {'oportunidad': oportunidad})