from django.db import migrations
from django.contrib.auth.hashers import make_password


datos_administradores = [
    dict(
        name="Luis Correa",
        email="lu.correab@duocuc.cl",
        username="lu.correab",
        rut="192140730",
        password="192140730"
    )
]

def crear_administradores(apps):
    Group = apps.get_model('auth', 'Group')
    User = apps.get_model('users', 'User')
    grupo_administrador = Group.objects.get(name="administrador")
    for datos_administrador in datos_administradores:
        password = datos_administrador.pop("password")
        administrador = User(**datos_administrador)
        administrador.password = make_password(password)
        administrador.save()
        administrador.groups.add(grupo_administrador)




def apply_migration(apps, schema_editor):
    crear_administradores(apps=apps)

def revert_migration(apps, schema_editor):
    User = apps.get_model('users', 'User')

    User.objects.all().delete()

class Migration(migrations.Migration):

    dependencies = [("users", "0006_user_empresa"), ("profesionales","0005_delete_servicio"), ("clientes","0005_facturamensual")]

    operations = [migrations.RunPython(apply_migration, revert_migration)]
