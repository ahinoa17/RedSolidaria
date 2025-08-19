# Importa el módulo de administración de Django
from django.contrib import admin
from django.contrib.auth.models import User, Group

# Importa los modelos del directorio actual
from .models import SolicitudPermutacion, HistorialPermutacion

# Registra el modelo en el panel de administración con configuración personalizada
@admin.register(SolicitudPermutacion)
class SolicitudPermutacionAdmin(admin.ModelAdmin):
    # Campos que se mostrarán en la lista de objetos en el admin
    list_display = ('solicitante', 'receptor', 'oportunidad_origen', 'oportunidad_destino', 'estado', 'fecha_creacion')
    
    # Filtros que aparecerán en la barra lateral
    list_filter = ('estado', 'fecha_creacion')
    
    # Campos por los que se puede realizar búsquedas
    search_fields = ('solicitante__username', 'receptor__username', 'oportunidad_origen__titulo', 'oportunidad_destino__titulo')
    
    # Jerarquía de navegación por fechas
    date_hierarchy = 'fecha_creacion'


@admin.register(HistorialPermutacion)
class HistorialPermutacionAdmin(admin.ModelAdmin):
    """
    Configuración del administrador para el historial de permutaciones.
    Solo accesible para superusuarios.
    """
    list_display = ('solicitud', 'get_accion_display', 'fecha', 'usuario')
    list_filter = ('accion', 'fecha')
    search_fields = ('solicitud__id', 'detalles', 'usuario__username')
    date_hierarchy = 'fecha'
    readonly_fields = ('solicitud', 'accion', 'detalles', 'fecha', 'usuario')
    
    def has_add_permission(self, request):
        # No permitir agregar manualmente registros de historial
        return False
        
    def has_delete_permission(self, request, obj=None):
        # Solo superusuarios pueden eliminar registros de historial
        return request.user.is_superuser
        
    def has_change_permission(self, request, obj=None):
        # No permitir editar registros de historial
        return False
        
    def get_queryset(self, request):
        # Por defecto, solo superusuarios pueden ver el historial
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.none()