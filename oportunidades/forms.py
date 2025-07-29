from django import forms
from .models import OportunidadVoluntariado

class OportunidadVoluntariadoForm(forms.ModelForm):
    class Meta:
        model = OportunidadVoluntariado
        fields = '__all__'