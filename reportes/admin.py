from django.contrib import admin
from .models import ReporteParticipacion

@admin.register(ReporteParticipacion)
class ReporteParticipacionAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'oportunidad', 'fecha_reporte', 'horas')
    list_filter = ('fecha_reporte',)
    search_fields = ('usuario__email', 'oportunidad__titulo')
    readonly_fields = ('fecha_creacion',)
    date_hierarchy = 'fecha_reporte'
