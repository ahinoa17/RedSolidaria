from django import forms
from .models import ReporteParticipacion

class ReporteParticipacionForm(forms.ModelForm):
    class Meta:
        model = ReporteParticipacion
        fields = ['oportunidad', 'horas']
        