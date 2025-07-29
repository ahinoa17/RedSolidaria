from django.contrib import admin
from .models import PermutacionParticipantes

@admin.register(PermutacionParticipantes)
class PermutacionParticipantesAdmin(admin.ModelAdmin):
    list_display = ('oportunidad', 'total_participantes', 'resultado_permutacion', 'fecha_calculo')
    search_fields = ('oportunidad__titulo',)
