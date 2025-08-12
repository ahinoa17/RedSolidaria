from django.contrib import admin
from .models import SolicitudPermutacion

@admin.register(SolicitudPermutacion)
class SolicitudPermutacionAdmin(admin.ModelAdmin):
    list_display = ('solicitante', 'receptor', 'oportunidad_origen', 'oportunidad_destino', 'estado', 'fecha_creacion')
    list_filter = ('estado', 'fecha_creacion')
    search_fields = ('solicitante__username', 'receptor__username', 'oportunidad_origen__titulo', 'oportunidad_destino__titulo')
    date_hierarchy = 'fecha_creacion'
