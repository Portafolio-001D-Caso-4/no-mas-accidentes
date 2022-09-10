# Generated by Django 3.2.15 on 2022-09-10 00:09

from django.db import migrations, models
import django.db.models.deletion
import no_mas_accidentes.users.validators


class Migration(migrations.Migration):

    dependencies = [
        ('servicios', '0005_agregar_fechas_checklist'),
    ]

    operations = [
        migrations.CreateModel(
            name='Participante',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254)),
                ('rut', models.CharField(max_length=9, validators=[no_mas_accidentes.users.validators.validar_rut])),
                ('asiste', models.BooleanField(default=False)),
                ('servicio', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='servicios.servicio')),
            ],
        ),
    ]