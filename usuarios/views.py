from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import RegistroForm, LoginForm

@login_required
def home(request):
    context = {
        'user': request.user
    }
    return render(request, 'home.html', context)

def registro_voluntario(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.tipo_usuario = 'voluntario'
            user.save()
            
            # Autenticar al usuario después del registro
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            user = authenticate(request, email=email, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, '¡Registro exitoso! Ahora eres un voluntario de la PUCE.')
                return redirect('home')  # Cambiado de 'inicio' a 'home'
    else:
        form = RegistroForm()
    
    return render(request, 'registration/registro.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')  # Usamos username para el campo de email
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, f'¡Bienvenido de nuevo, {user.nombre_completo}!')
                return redirect('home')  # Cambiado de 'inicio' a 'home'
            else:
                messages.error(request, 'Correo o contraseña incorrectos')
        else:
            messages.error(request, 'Por favor corrija los errores a continuación')
    else:
        form = LoginForm()
    
    return render(request, 'registration/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, 'Has cerrado sesión correctamente.')
    return redirect('login')
