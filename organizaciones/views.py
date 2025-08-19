# Importa utilidades para manejo de vistas y redirecciones
from django.shortcuts import render, get_object_or_404, redirect
# Importa decoradores para control de acceso
from django.contrib.auth.decorators import login_required, user_passes_test
# Importa el modelo Organizacion
from .models import Organizacion
# Importa el formulario personalizado
from .forms import OrganizacionForm

# Vista para listar todas las organizaciones
def lista_organizaciones(request):
    # Obtiene todas las organizaciones de la base de datos
    organizaciones = Organizacion.objects.all()
    # Renderiza la plantilla con la lista de organizaciones
    return render(request, 'organizaciones/lista.html', 
                {'organizaciones': organizaciones})

# Vista para mostrar los detalles de una organización específica
def detalle_organizacion(request, pk):
    # Obtiene la organización o devuelve 404 si no existe
    organizacion = get_object_or_404(Organizacion, pk=pk)
    # Renderiza la plantilla con los detalles de la organización
    return render(request, 'organizaciones/detalle.html', 
                {'organizacion': organizacion})

# Función auxiliar para verificar si un usuario es superusuario
def admin_requerido(user):
    return user.is_superuser or getattr(user, 'acceso_admin', False)

# Vista para crear una nueva organización
@login_required  # Requiere que el usuario esté autenticado
@user_passes_test(admin_requerido, login_url='lista_organizaciones')
def crear_organizacion(request):
    if request.method == 'POST':  # Si se envió el formulario
        # Crea una instancia del formulario con los datos enviados
        form = OrganizacionForm(request.POST)
        if form.is_valid():  # Valida los datos del formulario
            form.save()  # Guarda la nueva organización
            return redirect('lista_organizaciones')  # Redirige al listado
    else:
        # Muestra el formulario vacío
        form = OrganizacionForm()
    # Renderiza el formulario (válido o con errores)
    return render(request, 'organizaciones/form.html', {'form': form})

# Vista para editar una organización existente
@login_required
@user_passes_test(admin_requerido, login_url='lista_organizaciones')
def editar_organizacion(request, pk):
    # Obtiene la organización a editar
    organizacion = get_object_or_404(Organizacion, pk=pk)
    if request.method == 'POST':
        # Crea el formulario con los datos enviados y la instancia a editar
        form = OrganizacionForm(request.POST, instance=organizacion)
        if form.is_valid():
            form.save()  # Guarda los cambios
            return redirect('lista_organizaciones')
    else:
        # Muestra el formulario precargado con los datos actuales
        form = OrganizacionForm(instance=organizacion)
    return render(request, 'organizaciones/form.html', {'form': form})

# Vista para eliminar una organización
@login_required
@user_passes_test(admin_requerido, login_url='lista_organizaciones')
def eliminar_organizacion(request, pk):
    # Obtiene la organización a eliminar
    organizacion = get_object_or_404(Organizacion, pk=pk)
    if request.method == 'POST':  # Si se confirmó la eliminación
        organizacion.delete()  # Elimina la organización
        return redirect('lista_organizaciones')  # Redirige al listado
    # Muestra la página de confirmación si es GET
    return render(request, 'organizaciones/confirmar_eliminar.html', 
                {'organizacion': organizacion})