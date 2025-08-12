from django.contrib import admin
from .models import Inscripcion

@admin.register(Inscripcion)
class InscripcionAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'oportunidad', 'fecha_inscripcion', 'estado')
    list_filter = ('estado', 'fecha_inscripcion')
    search_fields = ('usuario__email', 'oportunidad__titulo')
    readonly_fields = ('fecha_inscripcion',)
    list_editable = ('estado',)
