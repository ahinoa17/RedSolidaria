from django.contrib import admin
from .models import ReporteParticipacion

@admin.register(ReporteParticipacion)
class ReporteParticipacionAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'oportunidad', 'horas', 'fecha_reporte')
    search_fields = ('usuario__username', 'oportunidad__titulo')
