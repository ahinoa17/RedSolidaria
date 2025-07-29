from django.shortcuts import render, get_object_or_404, redirect
from .models import Perfil
from .forms import PerfilForm
from django.contrib.auth.decorators import login_required

def home(request):
    # Renderiza el template home.html (debes tenerlo en templates/home.html)
    return render(request, 'home.html')

@login_required
def mi_perfil(request):
    perfil = get_object_or_404(Perfil, user=request.user)
    return render(request, 'usuarios/perfil.html', {'perfil': perfil})

@login_required
def editar_perfil(request):
    perfil = get_object_or_404(Perfil, user=request.user)
    if request.method == 'POST':
        form = PerfilForm(request.POST, instance=perfil)
        if form.is_valid():
            form.save()
            return redirect('mi_perfil')
    else:
        form = PerfilForm(instance=perfil)
    return render(request, 'usuarios/form.html', {'form': form})
