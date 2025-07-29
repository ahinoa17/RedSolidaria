from django import forms
from .models import Organizacion

class OrganizacionForm(forms.ModelForm):
    class Meta:
        model = Organizacion
        fields = ['nombre', 'descripcion', 'contacto_email', 'telefono', 'direccion']