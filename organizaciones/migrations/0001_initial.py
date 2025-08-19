# Generado automáticamente por Django 4.2.7
from django.db import migrations, models

class Migration(migrations.Migration):
    # Indica que es la migración inicial
    initial = True

    # Dependencias (vacío porque es la primera migración)
    dependencies = []

    # Operaciones a realizar
    operations = [
        migrations.CreateModel(
            name='Organizacion',  # Nombre del modelo
            fields=[
                # ID automático (clave primaria)
                ('id', models.BigAutoField(auto_created=True, primary_key=True, 
                                         serialize=False, verbose_name='ID')),
                
                # Nombre único de la organización
                ('nombre', models.CharField(max_length=100, unique=True)),
                
                # Descripción detallada
                ('descripcion', models.TextField()),
                
                # Email de contacto
                ('contacto_email', models.EmailField(max_length=254)),
                
                # Teléfono (opcional)
                ('telefono', models.CharField(blank=True, max_length=20)),
                
                # Dirección (opcional)
                ('direccion', models.CharField(blank=True, max_length=255)),
                
                # Ruta al archivo del logo (opcional)
                ('logo', models.CharField(
                    blank=True, 
                    help_text='Nombre del archivo del logo en static/img/logos/', 
                    max_length=100
                )),
                
                # Estado de la organización (activa/inactiva)
                ('activa', models.BooleanField(default=True)),
                
                # Fecha de creación (automática)
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                
                # Fecha de última actualización (automática)
                ('fecha_actualizacion', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]