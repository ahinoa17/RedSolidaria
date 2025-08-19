# Importación de módulos necesarios
from django import forms  # Para la creación de formularios
from django.core.exceptions import ValidationError  # Para manejar errores de validación
import re  # Para expresiones regulares
from .models import Organizacion  # Importa el modelo Organizacion


def validar_texto_con_sentido(texto, nombre_campo, min_palabras=2, min_caracteres=3):
    """
    Valida que el texto sea significativo y cumpla con ciertos criterios.
    Parámetros:
    - texto: El texto a validar
    - nombre_campo: Nombre del campo para mensajes de error personalizados
    - min_palabras: Número mínimo de palabras requeridas (por defecto 2)
    - min_caracteres: Longitud mínima de cada palabra (por defecto 3)
    """
    # Elimina espacios en blanco al inicio y final del texto
    texto = texto.strip()
    
    # Verifica que el texto no esté vacío
    if not texto:
        raise ValidationError(f"El campo {nombre_campo} es obligatorio.")
    
    # Verifica que el texto no consista solo en espacios en blanco
    if not texto.replace(" ", ""):
        raise ValidationError(f"El campo {nombre_campo} no puede contener solo espacios en blanco.")
    
    # Verifica que el texto contenga tanto vocales como consonantes
    tiene_vocales = any(vocal in texto.lower() for vocal in 'aeiouáéíóú')
    tiene_consonantes = any(c.isalpha() and c.lower() not in 'aeiouáéíóú' for c in texto)
    
    # Si falta alguna vocal o consonante, lanza un error
    if not tiene_vocales or not tiene_consonantes:
        raise ValidationError(
            f"Por favor ingrese un {nombre_campo} válido con palabras completas."
        )
    
    # Divide el texto en palabras filtrando las que son muy cortas
    palabras = [p for p in texto.split() if len(p) >= min_caracteres]
    # Verifica que haya suficientes palabras con la longitud mínima
    if len(palabras) < min_palabras:
        raise ValidationError(
            f"El campo {nombre_campo} debe contener al menos {min_palabras} "
            f"palabras de {min_caracteres} o más caracteres."
        )
    
    # Verifica que solo contenga caracteres permitidos
    if re.match(r'^[a-zA-Z0-9\s,.-áéíóúÁÉÍÓÚñÑ()°]+$', texto) is None:
        raise ValidationError(
            f"El campo {nombre_campo} contiene caracteres no permitidos. "
            "Solo se permiten letras, números, espacios y los siguientes caracteres: , . - ( ) °"
        )
    
    return texto  # Retorna el texto validado


class OrganizacionForm(forms.ModelForm):
    """
    Formulario para el modelo Organizacion.
    Define los campos, widgets y validaciones personalizadas.
    """
    class Meta:
        model = Organizacion  # Modelo asociado al formulario
        fields = ['nombre', 'descripcion', 'direccion', 'telefono']  # Campos a incluir
        # Configuración de widgets para personalizar la apariencia de los campos
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),  # Campo de texto simple
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),  # Área de texto
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),  # Campo de texto simple
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),  # Campo de texto simple
        }

    def clean_nombre(self):
        """Valida el campo nombre utilizando validar_texto_con_sentido"""
        nombre = self.cleaned_data.get('nombre', '')  # Obtiene el valor del campo
        try:
            return validar_texto_con_sentido(
                nombre,
                "nombre de la organización",  # Nombre descriptivo para mensajes de error
                min_palabras=2,  # Mínimo 2 palabras
                min_caracteres=3  # Mínimo 3 caracteres por palabra
            )
        except ValidationError as e:
            # Relanza la excepción con el mensaje de error
            raise ValidationError(str(e))

    def clean_direccion(self):
        """Valida el campo dirección utilizando validar_texto_con_sentido"""
        direccion = self.cleaned_data.get('direccion', '')  # Obtiene el valor del campo
        try:
            return validar_texto_con_sentido(
                direccion,
                "dirección",  # Nombre descriptivo para mensajes de error
                min_palabras=2,  # Mínimo 2 palabras
                min_caracteres=3  # Mínimo 3 caracteres por palabra
            )
        except ValidationError as e:
            # Relanza la excepción con el mensaje de error
            raise ValidationError(str(e))

    def clean_telefono(self):
        """Valida el formato del número de teléfono"""
        # Obtiene y limpia el valor del teléfono
        telefono = self.cleaned_data.get('telefono', '').strip()
        # Verifica que el teléfono tenga un formato válido
        # ^: inicio de la cadena
        # \+?: signo + opcional
        # [\d\s-]{8,15}: entre 8 y 15 dígitos, espacios o guiones
        # $: fin de la cadena
        if not re.match(r'^\+?[\d\s-]{8,15}$', telefono):
            raise ValidationError("Por favor ingrese un número de teléfono válido.")
        return telefono  # Retorna el teléfono validado