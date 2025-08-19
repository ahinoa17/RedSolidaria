# Importaciones estándar de Django
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout, get_user_model
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.http import require_http_methods
from django.db.models import Q
from django.core.paginator import Paginator
from .forms import RegistroForm, LoginForm, EditarUsuarioForm
from .models import Usuario

# Obtener el modelo de usuario personalizado
User = get_user_model()

# Función para verificar si el usuario es superusuario
def superusuario_requerido(user):
    return user.is_superuser


@login_required  # Decorador que requiere autenticación para acceder a la vista
def home(request):
    """
    Vista de la página de inicio del usuario autenticado.
    Muestra información personal del usuario.
    """
    # Contexto con el usuario actual para la plantilla
    context = {
        'user': request.user  # Usuario autenticado actualmente
    }
    # Renderiza la plantilla home.html con el contexto
    return render(request, 'home.html', context)


def registro_voluntario(request):
    """
    Vista para el registro de nuevos voluntarios.
    Maneja tanto la visualización del formulario (GET) como su procesamiento (POST).
    """
    if request.method == 'POST':  # Si el formulario ha sido enviado
        # Crea una instancia del formulario con los datos enviados
        form = RegistroForm(request.POST)
        
        # Valida los datos del formulario
        if form.is_valid():
            # Guarda el usuario sin hacer commit a la base de datos aún
            user = form.save(commit=False)
            # Asigna el tipo de usuario como 'voluntario'
            user.tipo_usuario = 'voluntario'
            # Guarda el usuario en la base de datos
            user.save()
            
            # Autenticar al usuario después del registro exitoso
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            user = authenticate(request, email=email, password=password)
            
            if user is not None:  # Si la autenticación fue exitosa
                # Inicia sesión al usuario
                login(request, user)
                # Muestra mensaje de éxito
                messages.success(request, '¡Registro exitoso! Ahora eres un voluntario de la PUCE.')
                # Redirige a la página de inicio
                return redirect('home')
    else:
        # Si es una petición GET, muestra el formulario vacío
        form = RegistroForm()
    
    # Renderiza la plantilla de registro con el formulario
    return render(request, 'registration/registro.html', {'form': form})


def login_view(request):
    """
    Vista para el inicio de sesión de usuarios.
    Maneja tanto la visualización del formulario (GET) como su procesamiento (POST).
    """
    if request.method == 'POST':  # Si el formulario ha sido enviado
        # Crea una instancia del formulario con los datos enviados
        form = LoginForm(request, data=request.POST)
        
        # Valida los datos del formulario
        if form.is_valid():
            # Obtiene el email (almacenado en el campo username del formulario)
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            # Autentica al usuario
            user = authenticate(request, email=email, password=password)
            
            if user is not None:  # Si la autenticación fue exitosa
                # Inicia sesión al usuario
                login(request, user)
                # Muestra mensaje de bienvenida personalizado
                messages.success(request, f'¡Bienvenido de nuevo, {user.nombre_completo}!')
                # Redirige a la página de inicio
                return redirect('home')
            else:
                # Muestra mensaje de error si la autenticación falla
                messages.error(request, 'Correo o contraseña incorrectos')
        else:
            # Muestra mensaje de error si hay errores en el formulario
            messages.error(request, 'Por favor corrija los errores a continuación')
    else:
        # Si es una petición GET, muestra el formulario vacío
        form = LoginForm()
    
    # Renderiza la plantilla de inicio de sesión con el formulario
    return render(request, 'registration/login.html', {'form': form})


def logout_view(request):
    """
    Vista para cerrar la sesión del usuario actual.
    """
    logout(request)  # Cierra la sesión del usuario
    messages.success(request, 'Has cerrado sesión correctamente.')  # Mensaje de confirmación
    return redirect('login')  # Redirige a la página de inicio de sesión


@login_required
@user_passes_test(superusuario_requerido)
def listar_usuarios(request):
    """
    Vista para listar todos los usuarios del sistema.
    Solo accesible para superusuarios.
    """
    # Mostrar mensajes si existen
    message_list = messages.get_messages(request)
    
    # Obtener parámetros de búsqueda
    query = request.GET.get('q', '')
    
    # Filtrar usuarios según la búsqueda
    usuarios = User.objects.all()
    if query:
        usuarios = usuarios.filter(
            Q(email__icontains=query) |
            Q(nombre_completo__icontains=query) |
            Q(tipo_usuario__icontains=query)
        )
    
    # Paginación
    paginator = Paginator(usuarios.order_by('-date_joined'), 10)  # 10 usuarios por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'query': query,
        'messages': message_list  # Asegurar que los mensajes estén disponibles en el contexto
    }
    return render(request, 'usuarios/listar_usuarios.html', context)


@login_required
@user_passes_test(superusuario_requerido)
def editar_usuario(request, usuario_id):
    """
    Vista para editar un usuario existente.
    Solo accesible para superusuarios.
    """
    # Limpiar mensajes existentes al inicio
    storage = messages.get_messages(request)
    storage.used = True
    
    usuario = get_object_or_404(User, id=usuario_id)
    acceso_admin_anterior = usuario.acceso_admin
    
    if request.method == 'POST':
        form = EditarUsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            try:
                # Guardar el formulario sin hacer commit para manejar la lógica de acceso_admin
                user = form.save(commit=False)
                
                # Si el usuario es superusuario, forzar acceso_admin a True
                if user.is_superuser:
                    user.acceso_admin = True
                
                # Guardar los cambios en el usuario
                user.save()
                
                # Guardar las relaciones many-to-many
                form.save_m2m()
                
                # Verificar si el acceso_admin cambió
                if acceso_admin_anterior != user.acceso_admin:
                    # Limpiar cualquier mensaje existente
                    storage = messages.get_messages(request)
                    storage.used = True
                    
                    if user.acceso_admin:
                        messages.success(request, f'Se ha otorgado acceso al panel de administración a {user.email}')
                    else:
                        messages.warning(request, f'Se ha revocado el acceso al panel de administración a {user.email}')
                
                return redirect('listar_usuarios')
                
            except Exception as e:
                # Limpiar mensajes existentes antes de mostrar el error
                storage = messages.get_messages(request)
                storage.used = True
                messages.error(request, f'Error al actualizar el usuario: {str(e)}')
    else:
        form = EditarUsuarioForm(instance=usuario)
    
    context = {
        'form': form,
        'usuario': usuario
    }
    return render(request, 'usuarios/editar_usuario.html', context)


@login_required
@user_passes_test(superusuario_requerido)
@require_http_methods(["POST"])
def toggle_estado_usuario(request, usuario_id):
    """
    Vista para activar/desactivar un usuario.
    Solo accesible para superusuarios y mediante POST.
    """
    if request.user.id == usuario_id:
        messages.error(request, 'No puedes desactivar tu propia cuenta.')
        return redirect('listar_usuarios')
    
    usuario = get_object_or_404(User, id=usuario_id)
    
    # No permitir desactivar superusuarios
    if usuario.is_superuser:
        messages.error(request, 'No se puede desactivar a un superusuario.')
        return redirect('listar_usuarios')
    
    # Cambiar el estado del usuario
    usuario.is_active = not usuario.is_active
    usuario.save()
    
    estado = 'activado' if usuario.is_active else 'desactivado'
    messages.success(request, f'El usuario {usuario.email} ha sido {estado} correctamente.')
    return redirect('listar_usuarios')
