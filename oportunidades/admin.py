from django.contrib import admin
from .models import OportunidadVoluntariado

@admin.register(OportunidadVoluntariado)
class OportunidadVoluntariadoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'organizacion', 'fecha_inicio', 'fecha_fin', 'estado', 'cupos')
    list_filter = ('estado', 'organizacion')
    search_fields = ('titulo', 'descripcion', 'ubicacion')
