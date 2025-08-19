# Importa el módulo forms de Django para crear formularios
from django import forms

# Importa el modelo Inscripcion del directorio actual
from .models import Inscripcion


# Define la clase del formulario que hereda de ModelForm
class InscripcionForm(forms.ModelForm):
    # Clase Meta para configurar el formulario
    class Meta:
        # Especifica el modelo en el que se basa el formulario
        model = Inscripcion
        
        # Lista de campos del modelo que se incluirán en el formulario
        # 'oportunidad': Relación con el modelo Oportunidad
        # 'comentarios': Campo de texto para notas adicionales
        fields = ['oportunidad', 'comentarios']