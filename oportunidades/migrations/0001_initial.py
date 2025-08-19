# Generado automáticamente por Django 4.2.7 el 2025-08-09
# Importa los módulos necesarios para las migraciones
from django.db import migrations, models
import django.db.models.deletion

# Define la clase de migración que hereda de migrations.Migration
class Migration(migrations.Migration):
    # Indica que es una migración inicial
    initial = True

    # Dependencias: esta migración depende de otra migración en la app 'organizaciones'
    dependencies = [
        ('organizaciones', '0001_initial'),
    ]

    # Operaciones que se realizarán en esta migración
    operations = [
        # Crea un nuevo modelo en la base de datos
        migrations.CreateModel(
            # Nombre del modelo
            name='OportunidadVoluntariado',
            # Campos del modelo
            fields=[
                # Campo ID automático como clave primaria
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                # Título de la oportunidad (máx. 150 caracteres)
                ('titulo', models.CharField(max_length=150)),
                # Descripción detallada (texto largo)
                ('descripcion', models.TextField()),
                # Fecha de inicio de la oportunidad
                ('fecha_inicio', models.DateField()),
                # Fecha de finalización de la oportunidad
                ('fecha_fin', models.DateField()),
                # Ubicación de la oportunidad (máx. 255 caracteres)
                ('ubicacion', models.CharField(max_length=255)),
                # Número de cupos disponibles (entero positivo)
                ('cupos', models.PositiveIntegerField()),
                # Estado de la oportunidad (Abierta o Cerrada)
                ('estado', models.CharField(
                    choices=[('abierta', 'Abierta'), ('cerrada', 'Cerrada')], 
                    default='abierta', 
                    max_length=20
                )),
                # Fecha de creación automática (se establece al crear)
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                # Relación con el modelo Organización (muchas oportunidades pertenecen a una organización)
                ('organizacion', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,  # Si se borra la organización, se borran sus oportunidades
                    to='organizaciones.organizacion'  # Referencia al modelo Organización
                )),
            ],
        ),
    ]