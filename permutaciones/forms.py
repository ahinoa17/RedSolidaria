from django import forms
from .models import PermutacionParticipantes

class PermutacionParticipantesForm(forms.ModelForm):
    class Meta:
        model = PermutacionParticipantes
        fields = ['oportunidad', 'total_participantes', 'resultado_permutacion']