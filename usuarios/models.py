# Importaciones estándar de Django
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import RegexValidator, EmailValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_puce_email(value):
    """
    Valida que el correo electrónico sea de dominio PUCE.
    
    Args:
        value (str): Correo electrónico a validar
        
    Raises:
        ValidationError: Si el correo no es de dominio @puce.edu.ec o @puce.ec
    """
    if not value.endswith(('@puce.edu.ec', '@puce.ec')):
        raise ValidationError(
            _('El correo electrónico debe ser de dominio @puce.edu.ec o @puce.ec')
        )


class UsuarioManager(BaseUserManager):
    """
    Gestor personalizado para el modelo Usuario.
    Implementa métodos para crear usuarios y superusuarios.
    """
    
    def create_user(self, email, password=None, **extra_fields):
        """
        Crea y guarda un usuario con el correo y contraseña proporcionados.
        
        Args:
            email (str): Correo electrónico del usuario
            password (str, optional): Contraseña en texto plano
            **extra_fields: Campos adicionales del modelo
            
        Returns:
            Usuario: Instancia del usuario creado
            
        Raises:
            ValueError: Si no se proporciona un correo electrónico
        """
        if not email:
            raise ValueError('El correo electrónico es obligatorio')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        """
        Crea y guarda un superusuario con el correo y contraseña proporcionados.
        
        Args:
            email (str): Correo electrónico del superusuario
            password (str, optional): Contraseña en texto plano
            **extra_fields: Campos adicionales del modelo
            
        Returns:
            Usuario: Instancia del superusuario creado
            
        Raises:
            ValueError: Si no se configuran correctamente los permisos de superusuario
        """
        # Establece valores por defecto para superusuario
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('tipo_usuario', 'admin')
        
        # Validaciones de superusuario
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser debe tener is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser debe tener is_superuser=True.')
        
        return self.create_user(email, password, **extra_fields)


class Usuario(AbstractUser):
    """
    Modelo de usuario personalizado que utiliza correo electrónico en lugar de nombre de usuario.
    Hereda de AbstractUser para aprovechar la autenticación de Django.
    """
    
    # Opciones para el campo tipo_usuario
    TIPO_USUARIO = [
        ('admin', 'Administrador'),
        ('voluntario', 'Voluntario'),
    ]
    
    # Eliminamos el campo username ya que usaremos email para autenticación
    username = None
    
    # Campo de correo electrónico con validación personalizada
    email = models.EmailField(
        'correo electrónico',
        unique=True,
        validators=[validate_puce_email],
        help_text='Correo institucional de la PUCE (@puce.edu.ec o @puce.ec)'
    )
    
    # Tipo de usuario (Administrador o Voluntario)
    tipo_usuario = models.CharField(
        'tipo de usuario',
        max_length=10,
        choices=TIPO_USUARIO,
        default='voluntario',
        help_text='Rol del usuario en el sistema'
    )
    
    # Campo de teléfono opcional con validación de formato
    telefono = models.CharField(
        'teléfono',
        max_length=15,
        validators=[
            RegexValidator(
                regex=r'^\+?1?\d{9,15}$',
                message="El número de teléfono debe tener entre 9 y 15 dígitos."
            )
        ],
        blank=True,
        null=True,
        help_text='Formato: +593987654321 (incluir código de país)'
    )
    
    # Nombre completo del usuario con validación de solo letras y espacios
    nombre_completo = models.CharField(
        'nombre completo',
        max_length=100,
        validators=[
            RegexValidator(
                regex=r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$',
                message="Solo se permiten letras y espacios en el nombre."
            )
        ],
        help_text='Nombre completo del usuario (solo letras y espacios)'
    )
    
    # Campo para controlar el acceso al panel de administración
    acceso_admin = models.BooleanField(
        'acceso al panel de administración',
        default=False,
        help_text='Indica si el usuario puede acceder al panel de administración.'
    )
    
    # Configuración de autenticación
    USERNAME_FIELD = 'email'  # Usar email para autenticación en lugar de username
    REQUIRED_FIELDS = ['nombre_completo']  # Campos requeridos al crear un usuario
    
    # Asignar el gestor personalizado
    objects = UsuarioManager()
    
    # Configuración de permisos (sobrescribiendo campos heredados para evitar conflictos)
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='grupos',
        blank=True,
        help_text='Los grupos a los que pertenece este usuario.',
        related_name='usuario_set',
        related_query_name='usuario',
    )
    
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='permisos de usuario',
        blank=True,
        help_text='Permisos específicos para este usuario.',
        related_name='usuario_set',
        related_query_name='usuario',
    )
    
    class Meta:
        """
        Clase Meta para configuraciones adicionales del modelo.
        """
        verbose_name = 'usuario'
        verbose_name_plural = 'usuarios'
        ordering = ['email']
    
    def __str__(self):
        """
        Representación en cadena del usuario.
        
        Returns:
            str: Correo electrónico y tipo de usuario
        """
        return f"{self.email} ({self.get_tipo_usuario_display()})"
    
    def save(self, *args, **kwargs):
        """
        Sobrescribe el método save para incluir validaciones adicionales
        y manejar los permisos de administrador.
        """
        from django.contrib.auth.models import Group, Permission
        
        # Validar correo para voluntarios
        if self.tipo_usuario == 'voluntario':
            validate_puce_email(self.email)
        
        # Obtener el estado anterior si es una edición
        if self.is_superuser:
            self.acceso_admin = True
            self.is_staff = True
        
        # Si el usuario tiene acceso_admin, asegurarse de que tenga is_staff = True
        if self.acceso_admin:
            self.is_staff = True
        
        # Guardar el usuario
        super().save(*args, **kwargs)
        
        # Obtener o crear el grupo de administradores
        from django.contrib.auth.models import Group, Permission
        from django.contrib.contenttypes.models import ContentType
        
        admin_group, created = Group.objects.get_or_create(name='Administradores')
        
        # Si el usuario tiene acceso_admin, agregarlo al grupo de administradores
        if self.acceso_admin and not self.is_superuser:
            self.groups.add(admin_group)
            
            # Asegurarse de que el grupo tenga los permisos necesarios
            if created:
                # Obtener todos los permisos de los modelos principales
                from django.contrib.auth.models import Permission
                from django.contrib.contenttypes.models import ContentType
                
                # Obtener todos los permisos de los modelos del proyecto
                content_types = ContentType.objects.filter(
                    app_label__in=['usuarios', 'oportunidades', 'inscripciones', 'organizaciones', 'permutaciones']
                )
                
                # Agregar todos los permisos al grupo
                for content_type in content_types:
                    permissions = Permission.objects.filter(content_type=content_type)
                    admin_group.permissions.add(*permissions)
            
            # Asegurarse de que el usuario tenga todos los permisos del grupo
            self.user_permissions.set(admin_group.permissions.all())
        elif not self.acceso_admin and not self.is_superuser:
            # Si se quita el acceso de administrador, quitar del grupo
            self.groups.remove(admin_group)
        
        # Si el usuario es superusuario, asegurarse de que tenga todos los permisos
        if self.is_superuser:
            self.is_staff = True
            self.is_superuser = True
            self.user_permissions.clear()
            self.groups.clear()
            
        # Guardar los cambios después de modificar grupos y permisos
        super().save(*args, **kwargs)
    
    def get_full_name(self):
        """
        Devuelve el nombre completo del usuario.
        """
        return self.nombre_completo
    
    def get_short_name(self):
        """
        Devuelve el nombre corto del usuario (primera parte del nombre completo).
        """
        return self.nombre_completo.split(' ')[0]
