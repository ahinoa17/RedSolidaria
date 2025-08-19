# Importaciones estándar de Django
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError

# Importación del modelo de Usuario personalizado
from .models import Usuario


class RegistroForm(UserCreationForm):
    """
    Formulario personalizado para el registro de nuevos usuarios.
    Hereda de UserCreationForm para aprovechar la validación de contraseñas.
    """
    
    # Campo de correo electrónico con validación personalizada
    email = forms.EmailField(
        label='Correo electrónico',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'usuario@puce.edu.ec'
        }),
        help_text='Debe ser un correo institucional de la PUCE (@puce.edu.ec o @puce.ec)'
    )
    
    # Campo para el nombre completo del usuario
    nombre_completo = forms.CharField(
        label='Nombre completo',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese su nombre completo'
        })
    )
    
    # Campo opcional para el teléfono
    telefono = forms.CharField(
        label='Teléfono (opcional)',
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '+593987654321'
        }),
        help_text='Formato: +593987654321 (incluir código de país)'
    )
    
    # Campo para la contraseña con widget de tipo contraseña
    password1 = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Cree una contraseña segura'
        }),
        help_text=(
            'La contraseña debe contener al menos 8 caracteres y no ser comúnmente utilizada.'
        )
    )
    
    # Campo para confirmar la contraseña
    password2 = forms.CharField(
        label='Confirmar contraseña',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Repita la contraseña'
        })
    )
    
    class Meta:
        """
        Clase Meta para configuraciones adicionales del formulario.
        """
        # Modelo al que está asociado el formulario
        model = Usuario
        # Campos que se mostrarán en el formulario, en el orden especificado
        fields = ('email', 'nombre_completo', 'telefono', 'password1', 'password2')
    
    def clean_email(self):
        """
        Valida que el correo electrónico sea institucional de la PUCE.
        
        Returns:
            str: El correo electrónico validado
            
        Raises:
            ValidationError: Si el correo no termina en @puce.edu.ec o @puce.ec
        """
        email = self.cleaned_data.get('email')
        if not email.endswith(('@puce.edu.ec', '@puce.ec')):
            raise ValidationError('Solo se permiten correos institucionales de la PUCE')
        return email


class LoginForm(AuthenticationForm):
    """
    Formulario personalizado para el inicio de sesión.
    Hereda de AuthenticationForm y personaliza los campos de autenticación.
    """
    # Sobrescribe el campo username para usar email en su lugar
    username = forms.EmailField(
        label='Correo electrónico',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'usuario@puce.edu.ec',
            'autofocus': True
        })
    )
    
    # Personaliza el campo de contraseña
    password = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese su contraseña'
        })
    )


class EditarUsuarioForm(forms.ModelForm):
    """
    Formulario para editar usuarios existentes.
    Permite modificar los campos básicos de un usuario.
    """
    class Meta:
        model = Usuario
        fields = ['email', 'nombre_completo', 'tipo_usuario', 'is_active', 'acceso_admin']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'nombre_completo': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo_usuario': forms.Select(attrs={'class': 'form-select'}),
            'acceso_admin': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Guardar el valor original del email
        if 'instance' in kwargs and kwargs['instance']:
            self.original_email = kwargs['instance'].email
            
            # Hacer que el campo de correo sea de solo lectura para evitar duplicados
            self.fields['email'].widget.attrs['readonly'] = True
            self.fields['email'].required = False  # No requerido ya que es de solo lectura
            
            # Si es un superusuario, no permitir modificar ciertos campos
            if kwargs['instance'].is_superuser:
                self.fields['is_active'].disabled = True
                self.fields['acceso_admin'].disabled = True
                self.fields['acceso_admin'].help_text = 'Los superusuarios siempre tienen acceso al panel de administración.'
        
        # Agregar clases de Bootstrap a los campos booleanos
        self.fields['is_active'].widget.attrs['class'] = 'form-check-input'
        self.fields['acceso_admin'].help_text = 'Permite el acceso al panel de administración de Django.'
    
    def clean_email(self):
        # Siempre devolver el email original para evitar cambios
        if hasattr(self, 'original_email'):
            return self.original_email
        return self.cleaned_data.get('email')
    
    def clean(self):
        cleaned_data = super().clean()
        # Asegurarse de que el email esté en los datos limpios
        if not cleaned_data.get('email') and hasattr(self, 'original_email'):
            cleaned_data['email'] = self.original_email
        return cleaned_data
