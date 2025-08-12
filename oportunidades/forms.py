from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
import re
from .models import OportunidadVoluntariado

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

class OportunidadVoluntariadoForm(forms.ModelForm):
    class Meta:
        model = OportunidadVoluntariado
        fields = [
            'titulo', 
            'descripcion', 
            'organizacion', 
            'ubicacion', 
            'fecha_inicio', 
            'fecha_fin',
            'horario',
            'requisitos',
            'beneficios',
            'cupos',
            'estado'
        ]
        widgets = {
            'fecha_inicio': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'fecha_fin': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'requisitos': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'beneficios': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'horario': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Lunes a Viernes, 9:00 AM - 5:00 PM'
            }),
            'organizacion': forms.Select(attrs={'class': 'form-select'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'ubicacion': forms.TextInput(attrs={'class': 'form-control'}),
            'cupos': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        }

    def clean_titulo(self):
        titulo = self.cleaned_data.get('titulo', '')
        try:
            return validar_texto_con_sentido(
                titulo,
                "título",
                min_palabras=2,
                min_caracteres=3
            )
        except ValidationError as e:
            raise ValidationError(str(e))

    def clean_ubicacion(self):
        ubicacion = self.cleaned_data.get('ubicacion', '')
        try:
            return validar_texto_con_sentido(
                ubicacion,
                "ubicación",
                min_palabras=2,
                min_caracteres=3
            )
        except ValidationError as e:
            raise ValidationError(str(e))

    def clean_descripcion(self):
        descripcion = self.cleaned_data.get('descripcion', '').strip()
        if len(descripcion) < 30:
            raise ValidationError("La descripción debe tener al menos 30 caracteres.")
        return descripcion

    def clean_requisitos(self):
        requisitos = self.cleaned_data.get('requisitos', '').strip()
        if len(requisitos) < 20:
            raise ValidationError("Por favor, proporcione una lista detallada de requisitos (mínimo 20 caracteres).")
        return requisitos

    def clean_beneficios(self):
        beneficios = self.cleaned_data.get('beneficios', '').strip()
        if len(beneficios) < 20:
            raise ValidationError("Por favor, describa los beneficios ofrecidos (mínimo 20 caracteres).")
        return beneficios

    def clean_horario(self):
        horario = self.cleaned_data.get('horario', '').strip()
        if not horario:
            raise ValidationError("Este campo es obligatorio.")
        if len(horario) < 10:
            raise ValidationError("Por favor, proporcione un horario más detallado (mínimo 10 caracteres).")
        return horario

    def clean_cupos(self):
        cupos = self.cleaned_data.get('cupos', 0)
        if cupos <= 0:
            raise ValidationError("El número de cupos debe ser mayor a cero.")
        return cupos

    def clean(self):
        cleaned_data = super().clean()
        fecha_inicio = cleaned_data.get('fecha_inicio')
        fecha_fin = cleaned_data.get('fecha_fin')

        if fecha_inicio and fecha_fin:
            if fecha_inicio < timezone.now().date():
                self.add_error('fecha_inicio', 'La fecha de inicio no puede ser en el pasado.')
            if fecha_fin < fecha_inicio:
                self.add_error('fecha_fin', 'La fecha de finalización no puede ser anterior a la fecha de inicio.')

        return cleaned_data