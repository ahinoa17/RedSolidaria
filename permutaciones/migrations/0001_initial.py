# Código generado automáticamente por Django 4.2.7 el 2025-08-09

# Importa los módulos necesarios para las migraciones
from django.db import migrations, models
import django.db.models.deletion

# Define la clase de migración
class Migration(migrations.Migration):
    # Indica si es la migración inicial
    initial = True

    # Dependencias: lista de migraciones que deben aplicarse antes
    dependencies = [
        # Depende de la migración inicial de la aplicación 'oportunidades'
        ('oportunidades', '0001_initial'),
    ]

    # Operaciones a realizar en esta migración
    operations = [
        # Crea un nuevo modelo en la base de datos
        migrations.CreateModel(
            name='PermutacionParticipantes',  # Nombre del modelo
            fields=[
                # Campo ID automático (clave primaria)
                ('id', models.BigAutoField(
                    auto_created=True,  # Se crea automáticamente
                    primary_key=True,   # Es la clave primaria
                    serialize=False,    # No se serializa
                    verbose_name='ID'   # Nombre legible
                )),
                # Campo para el total de participantes (entero positivo)
                ('total_participantes', models.PositiveIntegerField()),
                # Campo para el resultado de la permutación (entero grande)
                ('resultado_permutacion', models.BigIntegerField()),
                # Campo de fecha/hora que se establece automáticamente al crear
                ('fecha_calculo', models.DateTimeField(auto_now_add=True)),
                # Clave foránea que relaciona con el modelo OportunidadVoluntariado
                ('oportunidad', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,  # Eliminación en cascada
                    to='oportunidades.oportunidadvoluntariado'   # Modelo relacionado
                )),
            ],
        ),
    ]