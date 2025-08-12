from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import RegexValidator, EmailValidator
from django.core.exceptions import ValidationError  # Añade esta línea
from django.utils.translation import gettext_lazy as _

def validate_puce_email(value):
    if not value.endswith(('@puce.edu.ec', '@puce.ec')):
        raise ValidationError(
            _('El correo electrónico debe ser de dominio @puce.edu.ec o @puce.ec')
        )

class UsuarioManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('El correo electrónico es obligatorio')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('tipo_usuario', 'admin')

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser debe tener is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser debe tener is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class Usuario(AbstractUser):
    TIPO_USUARIO = [
        ('admin', 'Administrador'),
        ('voluntario', 'Voluntario'),
    ]
    
    username = None
    email = models.EmailField(
        'correo electrónico',
        unique=True,
        validators=[validate_puce_email]
    )
    
    tipo_usuario = models.CharField(
        max_length=10,
        choices=TIPO_USUARIO,
        default='voluntario'
    )
    
    telefono = models.CharField(
        max_length=15,
        validators=[
            RegexValidator(
                regex=r'^\+?1?\d{9,15}$',
                message="El número de teléfono debe tener entre 9 y 15 dígitos."
            )
        ],
        blank=True,
        null=True
    )
    
    nombre_completo = models.CharField(
        max_length=100,
        validators=[
            RegexValidator(
                regex=r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$',
                message="Solo se permiten letras y espacios en el nombre."
            )
        ]
    )

    # Campos requeridos
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nombre_completo']

    objects = UsuarioManager()

    # Agregando related_name personalizados para evitar conflictos
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name='usuario_set',
        related_query_name='usuario',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='usuario_set',
        related_query_name='usuario',
    )

    def __str__(self):
        return f"{self.email} ({self.get_tipo_usuario_display()})"

    def save(self, *args, **kwargs):
        # Si es voluntario, forzar que el correo sea de la PUCE
        if self.tipo_usuario == 'voluntario':
            validate_puce_email(self.email)
        super().save(*args, **kwargs)
