# Generated by Django 3.2.15 on 2022-09-09 23:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clientes', '0005_facturamensual'),
        ('servicios', '0003_evento'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChecklistBase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('items', models.JSONField()),
                ('empresa', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='clientes.empresa')),
                ('actualizado_en', models.DateTimeField(auto_now=True)),
                ('creado_en', models.DateTimeField(auto_now_add=True)),
            ]
        ),
        migrations.CreateModel(
            name='Checklist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('items', models.JSONField()),
                ('actualizado_en', models.DateTimeField(auto_now=True)),
                ('aplicado_en', models.DateTimeField(auto_now_add=True)),
                ('servicio', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='servicios.servicio')),
            ],
        ),
    ]
