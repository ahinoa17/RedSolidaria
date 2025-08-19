# Código generado automáticamente por Django 4.2.23 el 2025-08-11

# Importación de módulos necesarios
from django.conf import settings  # Para acceder a la configuración de Django
from django.db import migrations, models  # Para migraciones y modelos
import django.db.models.deletion  # Para relaciones entre modelos

# Clase de migración
class Migration(migrations.Migration):

    # Dependencias: migraciones que deben aplicarse antes
    dependencies = [
        # Migraciones previas necesarias
        ('oportunidades', '0002_alter_oportunidadvoluntariado_options_and_more'),
        # Dependencia del modelo de usuario configurado en settings
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        # Migración anterior de esta misma app
        ('permutaciones', '0002_solicitudpermutacion_delete_permutacionparticipantes'),
    ]

    # Operaciones a realizar en esta migración
    operations = [
        # Agrega un nuevo campo de fecha de actualización
        migrations.AddField(
            model_name='solicitudpermutacion',  # Modelo a modificar
            name='fecha_actualizacion',  # Nombre del nuevo campo
            field=models.DateTimeField(
                auto_now=True,  # Actualiza automáticamente al guardar
                verbose_name='Fecha de actualización'  # Nombre legible
            ),
        ),
        
        # Actualiza el campo 'estado' para incluir un nombre legible
        migrations.AlterField(
            model_name='solicitudpermutacion',
            name='estado',
            field=models.CharField(
                choices=[
                    ('pendiente', 'Pendiente'),
                    ('aceptada', 'Aceptada'),
                    ('rechazada', 'Rechazada'),
                    ('cancelada', 'Cancelada')
                ],
                default='pendiente',
                max_length=20,
                verbose_name='Estado'  # Nombre legible
            ),
        ),
        
        # Actualiza el campo 'fecha_creacion' para incluir un nombre legible
        migrations.AlterField(
            model_name='solicitudpermutacion',
            name='fecha_creacion',
            field=models.DateTimeField(
                auto_now_add=True,
                verbose_name='Fecha de creación'  # Nombre legible
            ),
        ),
        
        # Actualiza el campo 'mensaje' para incluir un nombre legible
        migrations.AlterField(
            model_name='solicitudpermutacion',
            name='mensaje',
            field=models.TextField(
                blank=True,
                null=True,
                verbose_name='Mensaje'  # Nombre legible
            ),
        ),
        
        # Actualiza las relaciones para incluir nombres legibles
        migrations.AlterField(
            model_name='solicitudpermutacion',
            name='oportunidad_destino',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='solicitudes_entrantes',
                to='oportunidades.oportunidadvoluntariado',
                verbose_name='Oportunidad de destino'  # Nombre legible
            ),
        ),
        
        migrations.AlterField(
            model_name='solicitudpermutacion',
            name='oportunidad_origen',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='solicitudes_salientes',
                to='oportunidades.oportunidadvoluntariado',
                verbose_name='Oportunidad de origen'  # Nombre legible
            ),
        ),
        
        migrations.AlterField(
            model_name='solicitudpermutacion',
            name='receptor',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='solicitudes_recibidas',
                to=settings.AUTH_USER_MODEL,
                verbose_name='Receptor'  # Nombre legible
            ),
        ),
        
        migrations.AlterField(
            model_name='solicitudpermutacion',
            name='solicitante',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='solicitudes_enviadas',
                to=settings.AUTH_USER_MODEL,
                verbose_name='Solicitante'  # Nombre legible
            ),
        ),
        
        # Agrega una restricción de unicidad para evitar solicitudes duplicadas
        migrations.AddConstraint(
            model_name='solicitudpermutacion',
            constraint=models.UniqueConstraint(
                condition=models.Q(('estado', 'pendiente')),
                fields=('solicitante', 'receptor', 'oportunidad_origen', 'oportunidad_destino', 'estado'),
                name='solicitud_permutacion_unica'
            ),
        ),
    ]