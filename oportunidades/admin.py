# Importa el módulo de administración de Django
from django.contrib import admin

# Importa el modelo OportunidadVoluntariado del directorio actual
from .models import OportunidadVoluntariado

# Registra el modelo en el panel de administración con configuración personalizada
@admin.register(OportunidadVoluntariado)
class OportunidadVoluntariadoAdmin(admin.ModelAdmin):
    # Campos que se mostrarán en la lista de objetos
    list_display = ('titulo', 'organizacion', 'fecha_inicio', 'fecha_fin', 'estado', 'cupos')
    
    # Filtros que aparecerán en la barra lateral
    list_filter = ('estado', 'organizacion')
    
    # Campos por los que se podrá buscar
    search_fields = ('titulo', 'descripcion', 'ubicacion')
