# Generado automáticamente por Django 4.2.23 el 2025-08-19 04:30

# Importaciones necesarias para la migración
import django.core.validators  # Para usar validadores de Django
from django.db import migrations, models  # Módulos para migraciones y modelos
import usuarios.models  # Importa modelos personalizados de la app usuarios

# Definición de la clase de migración
class Migration(migrations.Migration):

    # Dependencias: migraciones que deben aplicarse antes que esta
    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),  # Migración del sistema de autenticación
        ('usuarios', '0001_initial'),  # Migración inicial de la app usuarios
    ]

    # Operaciones que realizará esta migración
    operations = [
        # Cambia las opciones del modelo Usuario
        migrations.AlterModelOptions(
            name='usuario',  # Nombre del modelo a modificar
            # Nuevas opciones:
            # - Ordenar por email
            # - Nombres en singular y plural para el panel de administración
            options={'ordering': ['email'], 'verbose_name': 'usuario', 'verbose_name_plural': 'usuarios'},
        ),
        
        # Añade un nuevo campo al modelo Usuario
        migrations.AddField(
            model_name='usuario',  # Modelo al que se añade el campo
            name='acceso_admin',  # Nombre del nuevo campo
            # Campo booleano que indica si el usuario puede acceder al panel de administración
            field=models.BooleanField(
                default=False,  # Valor por defecto: falso
                help_text='Indica si el usuario puede acceder al panel de administración.',
                verbose_name='acceso al panel de administración'
            ),
        ),
        
        # Modifica el campo email del modelo Usuario
        migrations.AlterField(
            model_name='usuario',
            name='email',
            field=models.EmailField(
                help_text='Correo institucional de la PUCE (@puce.edu.ec o @puce.ec)',
                max_length=254,  # Longitud máxima para emails según RFC
                unique=True,  # No se permiten correos duplicados
                validators=[usuarios.models.validate_puce_email],  # Validador personalizado
                verbose_name='correo electrónico'  # Nombre legible
            ),
        ),
        
        # Modifica la relación groups del modelo Usuario
        migrations.AlterField(
            model_name='usuario',
            name='groups',
            field=models.ManyToManyField(
                blank=True,  # El campo puede estar vacío
                help_text='Los grupos a los que pertenece este usuario.',
                related_name='usuario_set',  # Nombre para la relación inversa
                related_query_name='usuario',  # Nombre para consultas inversas
                to='auth.group',  # Modelo con el que se relaciona
                verbose_name='grupos'  # Nombre legible
            ),
        ),
        
        # Modifica el campo nombre_completo del modelo Usuario
        migrations.AlterField(
            model_name='usuario',
            name='nombre_completo',
            field=models.CharField(
                help_text='Nombre completo del usuario (solo letras y espacios)',
                max_length=100,  # Longitud máxima del campo
                validators=[  # Validadores para el campo
                    django.core.validators.RegexValidator(
                        message='Solo se permiten letras y espacios en el nombre.',
                        regex='^[a-zA-ZáéíóúÁÉÍÓÚñÑ\\s]+$'  # Expresión regular que solo permite letras y espacios
                    )
                ],
                verbose_name='nombre completo'  # Nombre legible
            ),
        ),
        
        # Modifica el campo telefono del modelo Usuario
        migrations.AlterField(
            model_name='usuario',
            name='telefono',
            field=models.CharField(
                blank=True,  # El campo puede estar vacío
                help_text='Formato: +593987654321 (incluir código de país)',
                max_length=15,  # Longitud máxima para números internacionales
                null=True,  # Puede ser NULL en la base de datos
                validators=[  # Validador para el formato del teléfono
                    django.core.validators.RegexValidator(
                        message='El número de teléfono debe tener entre 9 y 15 dígitos.',
                        regex='^\\+?1?\\d{9,15}$'  # Expresión regular para validar teléfonos
                    )
                ],
                verbose_name='teléfono'  # Nombre legible
            ),
        ),
        
        # Modifica el campo tipo_usuario del modelo Usuario
        migrations.AlterField(
            model_name='usuario',
            name='tipo_usuario',
            field=models.CharField(
                choices=[  # Opciones disponibles para este campo
                    ('admin', 'Administrador'),
                    ('voluntario', 'Voluntario')
                ],
                default='voluntario',  # Valor por defecto
                help_text='Rol del usuario en el sistema',
                max_length=10,  # Longitud máxima
                verbose_name='tipo de usuario'  # Nombre legible
            ),
        ),
        
        # Modifica la relación user_permissions del modelo Usuario
        migrations.AlterField(
            model_name='usuario',
            name='user_permissions',
            field=models.ManyToManyField(
                blank=True,  # El campo puede estar vacío
                help_text='Permisos específicos para este usuario.',
                related_name='usuario_set',  # Nombre para la relación inversa
                related_query_name='usuario',  # Nombre para consultas inversas
                to='auth.permission',  # Modelo con el que se relaciona
                verbose_name='permisos de usuario'  # Nombre legible
            ),
        ),
    ]