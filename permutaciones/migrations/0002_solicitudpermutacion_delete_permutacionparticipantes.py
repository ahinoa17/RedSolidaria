# Código generado automáticamente por Django 4.2.7 el 2025-08-11

# Importación de módulos necesarios
from django.conf import settings  # Para acceder a la configuración de Django
from django.db import migrations, models  # Para migraciones y modelos
import django.db.models.deletion  # Para relaciones entre modelos

# Clase de migración
class Migration(migrations.Migration):

    # Dependencias: migraciones que deben aplicarse antes
    dependencies = [
        # Migración previa en la app 'oportunidades'
        ('oportunidades', '0002_alter_oportunidadvoluntariado_options_and_more'),
        # Dependencia del modelo de usuario configurado en settings
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        # Migración inicial de esta misma app
        ('permutaciones', '0001_initial'),
    ]

    # Operaciones a realizar en esta migración
    operations = [
        # Creación de un nuevo modelo
        migrations.CreateModel(
            name='SolicitudPermutacion',  # Nombre del modelo
            fields=[
                # Campo ID automático (clave primaria)
                ('id', models.BigAutoField(
                    auto_created=True,  # Se crea automáticamente
                    primary_key=True,   # Es la clave primaria
                    serialize=False,    # No se serializa
                    verbose_name='ID'   # Nombre legible
                )),
                # Campo de texto opcional para mensajes
                ('mensaje', models.TextField(blank=True, null=True)),
                # Campo de estado con opciones predefinidas
                ('estado', models.CharField(
                    choices=[  # Opciones posibles
                        ('pendiente', 'Pendiente'),
                        ('aceptada', 'Aceptada'),
                        ('rechazada', 'Rechazada'),
                        ('cancelada', 'Cancelada')
                    ],
                    default='pendiente',  # Valor por defecto
                    max_length=20         # Longitud máxima
                )),
                # Fecha de creación automática
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                
                # Relación con la oportunidad de destino
                ('oportunidad_destino', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,  # Eliminación en cascada
                    related_name='solicitudes_entrantes',  # Nombre de la relación inversa
                    to='oportunidades.oportunidadvoluntariado'  # Modelo relacionado
                )),
                # Relación con la oportunidad de origen
                ('oportunidad_origen', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='solicitudes_salientes',
                    to='oportunidades.oportunidadvoluntariado'
                )),
                # Relación con el usuario receptor
                ('receptor', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='solicitudes_recibidas',
                    to=settings.AUTH_USER_MODEL  # Modelo de usuario personalizado
                )),
                # Relación con el usuario solicitante
                ('solicitante', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='solicitudes_enviadas',
                    to=settings.AUTH_USER_MODEL
                )),
            ],
            # Opciones adicionales del modelo
            options={
                'verbose_name': 'solicitud de permutación',  # Nombre singular
                'verbose_name_plural': 'solicitudes de permutación',  # Nombre plural
                'ordering': ['-fecha_creacion'],  # Orden por defecto
            },
        ),
        
        # Eliminación del modelo antiguo
        migrations.DeleteModel(
            name='PermutacionParticipantes',  # Nombre del modelo a eliminar
        ),
    ]