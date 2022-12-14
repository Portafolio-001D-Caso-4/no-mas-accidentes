# Generated by Django 3.2.15 on 2022-09-08 04:34

import datetime
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clientes', '0003_agregar_profesional_asignado_y_telefono_a_empresa'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contrato',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('max_visitas_mensuales', models.PositiveIntegerField(default=2, validators=[django.core.validators.MaxValueValidator(100)])),
                ('max_capacitaciones_mensuales', models.PositiveIntegerField(default=2, validators=[django.core.validators.MaxValueValidator(100)])),
                ('max_asesorias_mensuales', models.PositiveIntegerField(default=10, validators=[django.core.validators.MaxValueValidator(100)])),
                ('inicio_horario_llamadas', models.TimeField(default=datetime.time(9, 0))),
                ('fin_horario_llamadas', models.TimeField(default=datetime.time(18, 0))),
                ('max_actualizaciones_mensuales_reporte_cliente', models.PositiveIntegerField(default=1, validators=[django.core.validators.MaxValueValidator(100)])),
                ('max_actualizaciones_checklist_anuales', models.PositiveIntegerField(default=2, validators=[django.core.validators.MaxValueValidator(100)])),
                ('dia_facturacion', models.PositiveIntegerField(default=28, validators=[django.core.validators.MaxValueValidator(28)])),
                ('valor_visita_extra', models.PositiveIntegerField(default=50000, validators=[django.core.validators.MaxValueValidator(1000000)])),
                ('valor_capacitacion_extra', models.PositiveIntegerField(default=100000, validators=[django.core.validators.MaxValueValidator(1000000)])),
                ('valor_asesoria_extra', models.PositiveIntegerField(default=100000, validators=[django.core.validators.MaxValueValidator(1000000)])),
                ('valor_llamada_fuera_horario', models.PositiveIntegerField(default=10000, validators=[django.core.validators.MaxValueValidator(1000000)])),
                ('valor_modificacion_checklist_extra', models.PositiveIntegerField(default=20000, validators=[django.core.validators.MaxValueValidator(1000000)])),
                ('valor_modificacion_reporte_extra', models.PositiveIntegerField(default=20000, validators=[django.core.validators.MaxValueValidator(1000000)])),
                ('valor_base', models.PositiveIntegerField(default=500000, validators=[django.core.validators.MaxValueValidator(10000000)])),
                ('esta_activo', models.BooleanField(default=True)),
                ('creado_en', models.DateTimeField(auto_now_add=True)),
                ('archivo', models.FileField(blank=True, null=True, upload_to='contratos/')),
                ('empresa', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='clientes.empresa')),
            ],
        ),
    ]
