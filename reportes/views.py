from django.shortcuts import render, get_object_or_404, redirect
from .models import ReporteParticipacion
from .forms import ReporteParticipacionForm
from django.contrib.auth.decorators import login_required

@login_required
def lista_reportes(request):
    reportes = ReporteParticipacion.objects.filter(usuario=request.user)
    return render(request, 'reportes/lista.html', {'reportes': reportes})

@login_required
def crear_reporte(request):
    if request.method == 'POST':
        form = ReporteParticipacionForm(request.POST)
        if form.is_valid():
            reporte = form.save(commit=False)
            reporte.usuario = request.user
            reporte.save()
            return redirect('lista_reportes')
    else:
        form = ReporteParticipacionForm()
    return render(request, 'reportes/form.html', {'form': form})

@login_required
def editar_reporte(request, pk):
    reporte = get_object_or_404(ReporteParticipacion, pk=pk, usuario=request.user)
    if request.method == 'POST':
        form = ReporteParticipacionForm(request.POST, instance=reporte)
        if form.is_valid():
            form.save()
            return redirect('lista_reportes')
    else:
        form = ReporteParticipacionForm(instance=reporte)
    return render(request, 'reportes/form.html', {'form': form})

@login_required
def eliminar_reporte(request, pk):
    reporte = get_object_or_404(ReporteParticipacion, pk=pk, usuario=request.user)
    if request.method == 'POST':
        reporte.delete()
        return redirect('lista_reportes')
    return render(request, 'reportes/confirmar_eliminar.html', {'reporte': reporte})