from django.shortcuts import render, get_object_or_404, redirect
from .models import Organizacion
from .forms import OrganizacionForm
from django.contrib.auth.decorators import login_required

def lista_organizaciones(request):
    organizaciones = Organizacion.objects.all()
    return render(request, 'organizaciones/lista.html', {'organizaciones': organizaciones})

def detalle_organizacion(request, pk):
    organizacion = get_object_or_404(Organizacion, pk=pk)
    return render(request, 'organizaciones/detalle.html', {'organizacion': organizacion})

@login_required
def crear_organizacion(request):
    if request.method == 'POST':
        form = OrganizacionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_organizaciones')
    else:
        form = OrganizacionForm()
    return render(request, 'organizaciones/form.html', {'form': form})

@login_required
def editar_organizacion(request, pk):
    organizacion = get_object_or_404(Organizacion, pk=pk)
    if request.method == 'POST':
        form = OrganizacionForm(request.POST, instance=organizacion)
        if form.is_valid():
            form.save()
            return redirect('lista_organizaciones')
    else:
        form = OrganizacionForm(instance=organizacion)
    return render(request, 'organizaciones/form.html', {'form': form})

@login_required
def eliminar_organizacion(request, pk):
    organizacion = get_object_or_404(Organizacion, pk=pk)
    if request.method == 'POST':
        organizacion.delete()
        return redirect('lista_organizaciones')
    return render(request, 'organizaciones/confirmar_eliminar.html', {'organizacion': organizacion})