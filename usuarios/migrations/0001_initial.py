# Generado por Django 4.2.7 el 2025-08-09 22:32
# Archivo de migración inicial para la aplicación de usuarios

# Importaciones estándar de Django
import django.core.validators
from django.db import migrations, models
import django.utils.timezone
# Importaciones locales
import usuarios.models


class Migration(migrations.Migration):
    """
    Migración inicial para el modelo de Usuario personalizado.
    Define la estructura de la tabla de usuarios en la base de datos.
    """

    # Indica que esta es la migración inicial
    initial = True

    # Dependencias de otras migraciones
    dependencies = [
        # Depende de la migración de autenticación de Django
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    # Operaciones a realizar en la base de datos
    operations = [
        # Creación de la tabla Usuario
        migrations.CreateModel(
            name='Usuario',
            fields=[
                # Campo ID autoincremental como clave primaria
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                
                # Campos heredados de AbstractBaseUser
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                
                # Campos heredados de PermissionsMixin
                ('is_superuser', models.BooleanField(
                    default=False, 
                    help_text='Designates that this user has all permissions without explicitly assigning them.',
                    verbose_name='superuser status'
                )),
                
                # Campos estándar de usuario de Django
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                
                # Campos de estado del usuario
                ('is_staff', models.BooleanField(
                    default=False,
                    help_text='Designates whether the user can log into this admin site.',
                    verbose_name='staff status'
                )),
                ('is_active', models.BooleanField(
                    default=True,
                    help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.',
                    verbose_name='active'
                )),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                
                # Campos personalizados
                
                # Email con validación personalizada para correos PUCE
                ('email', models.EmailField(
                    max_length=254, 
                    unique=True, 
                    validators=[usuarios.models.validate_puce_email], 
                    verbose_name='correo electrónico'
                )),
                
                # Tipo de usuario (Administrador o Voluntario)
                ('tipo_usuario', models.CharField(
                    choices=[
                        ('admin', 'Administrador'), 
                        ('voluntario', 'Voluntario')
                    ], 
                    default='voluntario', 
                    max_length=10
                )),
                
                # Teléfono con validación de formato
                ('telefono', models.CharField(
                    blank=True, 
                    max_length=15, 
                    null=True, 
                    validators=[
                        django.core.validators.RegexValidator(
                            message='El número de teléfono debe tener entre 9 y 15 dígitos.',
                            regex='^\\+?1?\\d{9,15}$'
                        )
                    ]
                )),
                
                # Nombre completo con validación de solo letras y espacios
                ('nombre_completo', models.CharField(
                    max_length=100, 
                    validators=[
                        django.core.validators.RegexValidator(
                            message='Solo se permiten letras y espacios en el nombre.',
                            regex='^[a-zA-ZáéíóúÁÉÍÓÚñÑ\\s]+$'
                        )
                    ]
                )),
                
                # Relaciones muchos a muchos con grupos y permisos
                ('groups', models.ManyToManyField(
                    blank=True,
                    help_text='The groups this user belongs to.',
                    related_name='usuario_set',
                    related_query_name='usuario',
                    to='auth.group',
                    verbose_name='groups'
                )),
                ('user_permissions', models.ManyToManyField(
                    blank=True,
                    help_text='Specific permissions for this user.',
                    related_name='usuario_set',
                    related_query_name='usuario',
                    to='auth.permission',
                    verbose_name='user permissions'
                )),
            ],
            # Opciones adicionales del modelo
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,  # No se puede crear una instancia directa de este modelo
            },
        ),
    ]
