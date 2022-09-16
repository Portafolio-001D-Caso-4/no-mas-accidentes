# Generated by Django 3.2.15 on 2022-09-16 03:54

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clientes', '0006_alter_contrato_archivo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='facturamensual',
            name='num_asesorias',
            field=models.PositiveIntegerField(default=0, validators=[django.core.validators.MaxValueValidator(1000)]),
        ),
        migrations.AlterField(
            model_name='facturamensual',
            name='num_asesorias_extra',
            field=models.PositiveIntegerField(default=0, validators=[django.core.validators.MaxValueValidator(1000)]),
        ),
        migrations.AlterField(
            model_name='facturamensual',
            name='num_capacitaciones',
            field=models.PositiveIntegerField(default=0, validators=[django.core.validators.MaxValueValidator(1000)]),
        ),
        migrations.AlterField(
            model_name='facturamensual',
            name='num_capacitaciones_extra',
            field=models.PositiveIntegerField(default=0, validators=[django.core.validators.MaxValueValidator(1000)]),
        ),
        migrations.AlterField(
            model_name='facturamensual',
            name='num_llamadas',
            field=models.PositiveIntegerField(default=0, validators=[django.core.validators.MaxValueValidator(1000)]),
        ),
        migrations.AlterField(
            model_name='facturamensual',
            name='num_llamadas_fuera_horario',
            field=models.PositiveIntegerField(default=0, validators=[django.core.validators.MaxValueValidator(1000)]),
        ),
        migrations.AlterField(
            model_name='facturamensual',
            name='num_modificaciones_checklist',
            field=models.PositiveIntegerField(default=0, validators=[django.core.validators.MaxValueValidator(100)]),
        ),
        migrations.AlterField(
            model_name='facturamensual',
            name='num_modificaciones_checklist_extra',
            field=models.PositiveIntegerField(default=0, validators=[django.core.validators.MaxValueValidator(100)]),
        ),
        migrations.AlterField(
            model_name='facturamensual',
            name='num_modificaciones_reporte',
            field=models.PositiveIntegerField(default=0, validators=[django.core.validators.MaxValueValidator(100)]),
        ),
        migrations.AlterField(
            model_name='facturamensual',
            name='num_modificaciones_reporte_extra',
            field=models.PositiveIntegerField(default=0, validators=[django.core.validators.MaxValueValidator(100)]),
        ),
        migrations.AlterField(
            model_name='facturamensual',
            name='num_visitas',
            field=models.PositiveIntegerField(default=0, validators=[django.core.validators.MaxValueValidator(1000)]),
        ),
        migrations.AlterField(
            model_name='facturamensual',
            name='num_visitas_extra',
            field=models.PositiveIntegerField(default=0, validators=[django.core.validators.MaxValueValidator(1000)]),
        ),
        migrations.AlterField(
            model_name='facturamensual',
            name='total',
            field=models.PositiveIntegerField(default=0, validators=[django.core.validators.MaxValueValidator(100000000)]),
        ),
    ]