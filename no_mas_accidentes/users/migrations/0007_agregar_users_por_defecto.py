from django.conf import settings
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


datos_profesionales = [
    {
        "datos_user":dict(
            name="Luis Portilla",
            email="lu.portilla@duocuc.cl",
            username="lu.portilla",
            rut="254186642",
            password="254186642"
        ),
        "datos_profesional":dict(
            telefono=959998656
        )
    }
]


def crear_profesionales(apps):
    Group = apps.get_model('auth', 'Group')
    User = apps.get_model('users', 'User')
    Profesional = apps.get_model('profesionales', 'Profesional')
    grupo_profesional = Group.objects.get(name="profesional")
    for datos_profesional in datos_profesionales:
        password = datos_profesional["datos_user"].pop("password")

        usuario = User(**datos_profesional["datos_user"])
        usuario.password = make_password(password)
        usuario.save()

        usuario.groups.add(grupo_profesional)

        profesional = Profesional(usuario=usuario, **datos_profesional["datos_profesional"])
        profesional.save()


datos_clientes = [
    {
        "datos_user":dict(
            name="Juan Robles",
            email="ju.roblesb@duocuc.cl",
            username="ju.roblesb",
            rut="250474474",
            password="250474474"
        ),
        "datos_empresa":dict(
            rut="96928510",
            nombre="EMPRESAS LIPIGAS S.A.",
            giro="VENTA AL POR MENOR DE GAS LICUADO EN BOMBONAS (CILINDROS)",
            direccion="AV. APOQUINDO 5400 PISO 15",
            latitud=None,
            longitud=None,
            esta_activa=True,
            telefono=955347157,
            profesional_asignado_rut=254186642
        )
    }
]
def crear_clientes(apps):
    Group = apps.get_model('auth', 'Group')
    User = apps.get_model('users', 'User')
    Empresa = apps.get_model('clientes', 'Empresa')
    Contrato = apps.get_model('clientes', 'Contrato')
    Profesional = apps.get_model('profesionales', 'Profesional')

    grupo_cliente = Group.objects.get(name="cliente")
    for datos_cliente in datos_clientes:
        profesional_asignado_rut = datos_cliente["datos_empresa"].pop("profesional_asignado_rut")
        profesional = Profesional.objects.get(usuario__rut=profesional_asignado_rut)

        empresa = Empresa(**datos_cliente["datos_empresa"])
        empresa.profesional_asignado = profesional
        empresa.save()

        contrato = Contrato(empresa=empresa)
        contrato.save()

        password = datos_cliente["datos_user"].pop("password")
        usuario = User(**datos_cliente["datos_user"])
        usuario.password = make_password(password)
        usuario.empresa = empresa
        usuario.save()

        usuario.groups.add(grupo_cliente)



def apply_migration(apps, schema_editor):
    crear_administradores(apps=apps)
    crear_profesionales(apps=apps)
    crear_clientes(apps=apps)


def revert_migration(apps, schema_editor):
    User = apps.get_model('users', 'User')
    Empresa = apps.get_model('clientes', 'Empresa')
    Profesional = apps.get_model('profesionales', 'Profesional')
    Contrato = apps.get_model('clientes', 'Contrato')

    User.objects.all().delete()
    Empresa.objects.all().delete()
    Profesional.objects.all().delete()
    Contrato.objects.all().delete()

class Migration(migrations.Migration):

    dependencies = [("users", "0006_user_empresa"), ("profesionales","0005_delete_servicio"), ("clientes","0005_facturamensual")]

    operations = [migrations.RunPython(apply_migration, revert_migration)]
