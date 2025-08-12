# organizaciones/forms.py
from django import forms
from django.core.exceptions import ValidationError
import re
from .models import Organizacion

def validar_texto_con_sentido(texto, nombre_campo, min_palabras=2, min_caracteres=3):
    """
    Valida que el texto tenga sentido (no solo espacios o caracteres aleatorios)
    - min_palabras: mínimo de palabras requeridas
    - min_caracteres: mínimo de caracteres por palabra
    """
    # Eliminar espacios al inicio y final
    texto = texto.strip()
    
    # Verificar que no esté vacío
    if not texto:
        raise ValidationError(f"El campo {nombre_campo} es obligatorio.")
    
    # Verificar que no sean solo espacios
    if not texto.replace(" ", ""):
        raise ValidationError(f"El campo {nombre_campo} no puede contener solo espacios en blanco.")
    
    # Verificar que no sean caracteres aleatorios (sin vocales o sin consonantes)
    tiene_vocales = any(vocal in texto.lower() for vocal in 'aeiouáéíóú')
    tiene_consonantes = any(c.isalpha() and c.lower() not in 'aeiouáéíóú' for c in texto)
    
    if not tiene_vocales or not tiene_consonantes:
        raise ValidationError(
            f"Por favor ingrese un {nombre_campo} válido con palabras completas."
        )
    
    # Dividir en palabras y verificar longitud mínima
    palabras = [p for p in texto.split() if len(p) >= min_caracteres]
    if len(palabras) < min_palabras:
        raise ValidationError(
            f"El campo {nombre_campo} debe contener al menos {min_palabras} "
            f"palabras de {min_caracteres} o más caracteres."
        )
    
    # Verificar caracteres permitidos
    if re.match(r'^[a-zA-Z0-9\s,.-áéíóúÁÉÍÓÚñÑ()°]+$', texto) is None:
        raise ValidationError(
            f"El campo {nombre_campo} contiene caracteres no permitidos. "
            "Solo se permiten letras, números, espacios y los siguientes caracteres: , . - ( ) °"
        )
    
    return texto

class OrganizacionForm(forms.ModelForm):
    class Meta:
        model = Organizacion
        fields = ['nombre', 'descripcion', 'direccion', 'telefono']  # Solo campos que existen
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre', '')
        try:
            return validar_texto_con_sentido(
                nombre,
                "nombre de la organización",
                min_palabras=2,
                min_caracteres=3
            )
        except ValidationError as e:
            raise ValidationError(str(e))

    def clean_direccion(self):
        direccion = self.cleaned_data.get('direccion', '')
        try:
            return validar_texto_con_sentido(
                direccion,
                "dirección",
                min_palabras=2,
                min_caracteres=3
            )
        except ValidationError as e:
            raise ValidationError(str(e))

    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono', '').strip()
        # Validar formato de teléfono
        if not re.match(r'^\+?[\d\s-]{8,15}$', telefono):
            raise ValidationError("Por favor ingrese un número de teléfono válido.")
        return telefono