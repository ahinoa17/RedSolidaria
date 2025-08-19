# Importa el módulo forms de Django para la creación de formularios
from django import forms

# Importa el modelo PermutacionParticipantes del directorio actual
from .models import PermutacionParticipantes

# Define un formulario basado en el modelo PermutacionParticipantes
class PermutacionParticipantesForm(forms.ModelForm):
    # Clase Meta para configurar el formulario
    class Meta:
        # Especifica el modelo en el que se basa el formulario
        model = PermutacionParticipantes
        
        # Campos del modelo que se incluirán en el formulario
        fields = ['oportunidad', 'total_participantes', 'resultado_permutacion']