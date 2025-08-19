# Importaciones de Django
from django.contrib import admin
from .models import Inscripcion


@admin.register(Inscripcion)
class InscripcionAdmin(admin.ModelAdmin):
    """
    Configuración del panel de administración para el modelo Inscripcion.
    
    Permite gestionar las inscripciones de los voluntarios a las oportunidades
    de voluntariado directamente desde el panel de administración de Django.
    """
    
    # Campos que se mostrarán en la lista de objetos
    list_display = ('usuario', 'oportunidad', 'fecha_inscripcion', 'estado')
    
    # Filtros laterales para filtrar las inscripciones
    list_filter = ('estado', 'fecha_inscripcion')
    
    # Campos por los que se puede buscar
    search_fields = ('usuario__email', 'oportunidad__titulo')
    
    # Campos de solo lectura (no editables)
    readonly_fields = ('fecha_inscripcion',)
    
    # Campos editables directamente desde la lista de objetos
    list_editable = ('estado',)