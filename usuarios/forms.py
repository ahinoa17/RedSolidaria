from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from .models import Usuario

class RegistroForm(UserCreationForm):
    email = forms.EmailField(
        label='Correo electrónico',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'usuario@puce.edu.ec'}),
        help_text='Debe ser un correo institucional de la PUCE (@puce.edu.ec o @puce.ec)'
    )
    
    nombre_completo = forms.CharField(
        label='Nombre completo',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    telefono = forms.CharField(
        label='Teléfono (opcional)',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        help_text='Formato: +593987654321'
    )
    
    password1 = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    
    password2 = forms.CharField(
        label='Confirmar contraseña',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = Usuario
        fields = ('email', 'nombre_completo', 'telefono', 'password1', 'password2')
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email.endswith(('@puce.edu.ec', '@puce.ec')):
            raise ValidationError('Solo se permiten correos institucionales de la PUCE')
        return email

class LoginForm(AuthenticationForm):
    username = forms.EmailField(
        label='Correo electrónico',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'usuario@puce.edu.ec'})
    )
    password = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
