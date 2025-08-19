# Generado automáticamente por Django 4.2.7 el 2025-08-10

# Importa los módulos necesarios para las migraciones
from django.db import migrations, models

# Define la clase de migración que hereda de migrations.Migration
class Migration(migrations.Migration):
    # Especifica las migraciones que deben aplicarse antes que esta
    dependencies = [
        ('oportunidades', '0001_initial'),  # Depende de la migración inicial de la app oportunidades
    ]

    # Operaciones que se realizarán en esta migración
    operations = [
        # Modifica las opciones del modelo OportunidadVoluntariado
        migrations.AlterModelOptions(
            name='oportunidadvoluntariado',
            options={
                'ordering': ['-fecha_creacion'],  # Ordena por fecha de creación descendente
                'verbose_name': 'Oportunidad de Voluntariado',  # Nombre singular en el admin
                'verbose_name_plural': 'Oportunidades de Voluntariado'  # Nombre plural en el admin
            },
        ),
        
        # Añade el campo 'beneficios' al modelo
        migrations.AddField(
            model_name='oportunidadvoluntariado',
            name='beneficios',
            field=models.TextField(
                blank=True,  # El campo puede estar vacío
                default='',  # Valor por defecto: cadena vacía
                help_text='Describe los beneficios que ofrece el voluntariado'  # Texto de ayuda en el formulario
            ),
        ),
        
        # Añade el campo 'horario' al modelo
        migrations.AddField(
            model_name='oportunidadvoluntariado',
            name='horario',
            field=models.CharField(
                blank=True,  # El campo puede estar vacío
                default='',  # Valor por defecto: cadena vacía
                help_text='Ej: Lunes a Viernes, 9:00 AM - 5:00 PM',  # Ejemplo de formato
                max_length=100  # Longitud máxima del campo
            ),
        ),
        
        # Añade el campo 'requisitos' al modelo
        migrations.AddField(
            model_name='oportunidadvoluntariado',
            name='requisitos',
            field=models.TextField(
                blank=True,  # El campo puede estar vacío
                default='',  # Valor por defecto: cadena vacía
                help_text='Lista los requisitos necesarios para el voluntariado'  # Texto de ayuda
            ),
        ),
    ]