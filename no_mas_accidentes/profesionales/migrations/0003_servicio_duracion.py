# Generated by Django 3.2.15 on 2022-09-09 20:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profesionales', '0002_servicio'),
    ]

    operations = [
        migrations.AddField(
            model_name='servicio',
            name='duracion',
            field=models.DurationField(blank=True, null=True),
        ),
    ]
