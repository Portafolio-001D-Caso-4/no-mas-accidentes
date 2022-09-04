from django.conf import settings
from django.db import migrations


def apply_migration(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Group.objects.bulk_create([
        Group(name='cliente'),
        Group(name='administrador'),
        Group(name='profesional'),
    ], ignore_conflicts=True)


def revert_migration(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Group.objects.filter(
        name__in=[
            'cliente',
            'administrador',
            'profesional',
        ]
    ).delete()



class Migration(migrations.Migration):

    dependencies = [("users", "0001_initial")]

    operations = [migrations.RunPython(apply_migration, revert_migration)]
