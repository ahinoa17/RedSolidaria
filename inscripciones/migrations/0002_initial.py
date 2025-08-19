# Generado automáticamente por Django 4.2.7 el 2025-08-09
# Segunda migración para la aplicación 'inscripciones' que añade relaciones adicionales

# Importaciones necesarias
from django.conf import settings  # Para acceder a la configuración de Django
from django.db import migrations, models  # Para las operaciones de migración
import django.db.models.deletion  # Para las relaciones entre modelos

class Migration(migrations.Migration):
    # Indica que esta es una migración inicial (aunque es la segunda, probablemente se generó en un mismo proceso)
    initial = True

    # Dependencias de esta migración
    dependencies = [
        ('inscripciones', '0001_initial'),  # Depende de la migración anterior
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),  # Depende del modelo de usuario configurado
    ]

    # Operaciones que se realizarán al aplicar esta migración
    operations = [
        # Añade un nuevo campo 'usuario' al modelo Inscripcion
        migrations.AddField(
            model_name='inscripcion',  # Modelo al que se le añade el campo
            name='usuario',  # Nombre del nuevo campo
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,  # Si se elimina el usuario, se eliminan sus inscripciones
                to=settings.AUTH_USER_MODEL,  # Relación con el modelo de usuario
                verbose_name='usuario'  # Nombre legible para el panel de administración
            ),
        ),
        
        # Añade una restricción de unicidad compuesta
        migrations.AlterUniqueTogether(
            name='inscripcion',  # Modelo al que se aplica la restricción
            unique_together={('usuario', 'oportunidad')},  # Un usuario solo puede inscribirse una vez por oportunidad
        ),
    ]
