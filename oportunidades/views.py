# Importaciones de Django y utilidades
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import OportunidadVoluntariado
from .forms import OportunidadVoluntariadoForm

# Función auxiliar para verificar si un usuario es superusuario
def admin_requerido(user):
    return user.is_superuser or getattr(user, 'acceso_admin', False)

# Vista para listar todas las oportunidades
def lista_oportunidades(request):
    # Obtiene todas las oportunidades de la base de datos
    oportunidades = OportunidadVoluntariado.objects.all()
    
    # Verifica si el usuario está autenticado y no es superusuario
    if request.user.is_authenticated and not request.user.is_superuser:
        # Obtiene las IDs de las oportunidades en las que el usuario está inscrito
        inscripciones_usuario = list(
            request.user.inscripcion_set
            .select_related('oportunidad')
            .values_list('oportunidad_id', flat=True)
        )
    else:
        inscripciones_usuario = []
    
    # Renderiza la plantilla con el contexto
    return render(request, 'oportunidades/lista.html', {
        'oportunidades': oportunidades,
        'inscripciones_usuario': inscripciones_usuario
    })

# Vista para ver el detalle de una oportunidad específica
def detalle_oportunidad(request, pk):
    # Obtiene la oportunidad o devuelve 404 si no existe
    oportunidad = get_object_or_404(OportunidadVoluntariado, pk=pk)
    
    # Verifica si el usuario actual está inscrito en esta oportunidad
    esta_inscrito = False
    if request.user.is_authenticated and not request.user.is_superuser:
        esta_inscrito = request.user.inscripcion_set.filter(
            oportunidad=oportunidad
        ).exists()
    
    # Renderiza la plantilla con el contexto
    return render(request, 'oportunidades/detalle.html', {
        'oportunidad': oportunidad,
        'esta_inscrito': esta_inscrito
    })

# Vista para crear una nueva oportunidad (requiere autenticación y ser superusuario)
@login_required
@user_passes_test(admin_requerido, login_url='lista_oportunidades')
def crear_oportunidad(request):
    if request.method == 'POST':
        # Procesa el formulario enviado
        form = OportunidadVoluntariadoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_oportunidades')
    else:
        # Muestra el formulario vacío
        form = OportunidadVoluntariadoForm()
    return render(request, 'oportunidades/form.html', {'form': form})

# Vista para editar una oportunidad existente
@login_required
@user_passes_test(admin_requerido, login_url='lista_oportunidades')
def editar_oportunidad(request, pk):
    # Obtiene la oportunidad a editar
    oportunidad = get_object_or_404(OportunidadVoluntariado, pk=pk)
    
    if request.method == 'POST':
        # Procesa el formulario con los datos existentes
        form = OportunidadVoluntariadoForm(request.POST, instance=oportunidad)
        if form.is_valid():
            form.save()
            return redirect('detalle_oportunidad', pk=pk)
    else:
        # Muestra el formulario con los datos actuales
        form = OportunidadVoluntariadoForm(instance=oportunidad)
    return render(request, 'oportunidades/form.html', {'form': form})

# Vista para eliminar una oportunidad
@login_required
@user_passes_test(admin_requerido, login_url='lista_oportunidades')
def eliminar_oportunidad(request, pk):
    # Obtiene la oportunidad a eliminar
    oportunidad = get_object_or_404(OportunidadVoluntariado, pk=pk)
    
    if request.method == 'POST':
        # Elimina la oportunidad
        oportunidad.delete()
        return redirect('lista_oportunidades')
    
    # Muestra la página de confirmación
    return render(request, 'oportunidades/confirmar_eliminar.html', {
        'oportunidad': oportunidad
    })