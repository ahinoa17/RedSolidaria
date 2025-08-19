# Generado automáticamente por Django 4.2.7 el 2025-08-09
# Este archivo representa la migración inicial para la aplicación 'inscripciones'

# Importaciones necesarias para las migraciones de Django
from django.db import migrations, models
import django.db.models.deletion

# Clase de migración generada automáticamente
class Migration(migrations.Migration):
    # Indica que esta es la migración inicial de la aplicación
    initial = True

    # Dependencias de esta migración
    # En este caso, depende de la migración inicial de la aplicación 'oportunidades'
    dependencies = [
        ('oportunidades', '0001_initial'),
    ]

    # Operaciones que se realizarán al aplicar esta migración
    operations = [
        migrations.CreateModel(
            # Define un nuevo modelo llamado 'Inscripcion'
            name='Inscripcion',
            # Campos del modelo
            fields=[
                # Campo ID automático (clave primaria)
                ('id', models.BigAutoField(
                    auto_created=True, 
                    primary_key=True, 
                    serialize=False, 
                    verbose_name='ID'
                )),
                # Fecha de inscripción que se establece automáticamente al crear el registro
                ('fecha_inscripcion', models.DateTimeField(auto_now_add=True)),
                # Estado de la inscripción con opciones predefinidas
                ('estado', models.CharField(
                    choices=[
                        ('pendiente', 'Pendiente'), 
                        ('aceptada', 'Aceptada'), 
                        ('rechazada', 'Rechazada'), 
                        ('completada', 'Completada')
                    ], 
                    default='pendiente', 
                    max_length=20
                )),
                # Campo para comentarios opcionales
                ('comentarios', models.TextField(blank=True, null=True)),
                # Clave foránea que relaciona con el modelo OportunidadVoluntariado
                ('oportunidad', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE, 
                    to='oportunidades.oportunidadvoluntariado', 
                    verbose_name='oportunidad'
                )),
            ],
            # Configuraciones adicionales del modelo
            options={
                'verbose_name': 'inscripción',  # Nombre singular en el admin
                'verbose_name_plural': 'inscripciones',  # Nombre plural en el admin
            },
        ),
    ]