import datetime

import arrow
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand
from django.db import transaction

# from no_mas_accidentes.clientes.business_logic.reportes import actualizar_reporte_cliente, traer_reporte_cliente
from no_mas_accidentes.clientes.models import Contrato, Empresa, FacturaMensual
from no_mas_accidentes.profesionales.models import Profesional
from no_mas_accidentes.servicios.business_logic.reportes import (
    actualizar_reporte_cliente,
)
from no_mas_accidentes.servicios.constants import (
    TiposDeServicio,
    duracion_en_hrs_por_servicio,
)
from no_mas_accidentes.servicios.models import (
    ChecklistBase,
    Evento,
    Participante,
    Servicio,
)
from no_mas_accidentes.users.models import User


def cargar_capacitaciones_para_empresa(empresa_id: int, mes: str):
    empresa = Empresa.objects.get(id=empresa_id)
    profesional = empresa.profesional_asignado

    # 1. capacitacion 15/01/2022
    capacitacion = Servicio(
        tipo=TiposDeServicio.CAPACITACION,
        profesional=profesional,
        empresa=empresa,
        agendado_para=arrow.get(f"2022-{mes}-15T15:00:00+00:00").datetime,
        realizado_en=arrow.get(f"2022-{mes}-15T15:00:00+00:00").datetime,
        duracion=datetime.timedelta(
            hours=duracion_en_hrs_por_servicio[TiposDeServicio.CAPACITACION]
        ),
        motivo="Capacitación sobre nueva ley 2022",
        contenido="Ley 2022 y sus artículos relacionados al rubro",
        num_participantes=3,
    )
    capacitacion.save()
    capacitacion.creado_en = arrow.get(f"2022-{mes}-10T15:00:00+00:00").datetime
    capacitacion.save(update_fields=["creado_en"])
    participante_1 = Participante(
        nombre="Luis Correa",
        email="l.correa.bruna@gmail.com",
        rut="192140730",
        asiste=True,
        servicio=capacitacion,
    )
    participante_2 = Participante(
        nombre="Juan Robles",
        email="jurobles@gmail.com",
        rut="13338250K",
        asiste=True,
        servicio=capacitacion,
    )
    participante_3 = Participante(
        nombre="Luis Portilla",
        email="luportilla@gmail.com",
        rut="136530682",
        asiste=False,
        servicio=capacitacion,
    )
    Participante.objects.bulk_create([participante_1, participante_3, participante_2])

    # 2. capacitacion 20/01/2022
    capacitacion = Servicio(
        tipo=TiposDeServicio.CAPACITACION,
        profesional=profesional,
        empresa=empresa,
        agendado_para=arrow.get(f"2022-{mes}-20T10:00:00+00:00").datetime,
        realizado_en=arrow.get(f"2022-{mes}-20T10:00:00+00:00").datetime,
        duracion=datetime.timedelta(
            hours=duracion_en_hrs_por_servicio[TiposDeServicio.CAPACITACION]
        ),
        motivo="Capacitación sobre nuevas políticas laborales",
        contenido="Nuevas políticas a aplicar a empresas del rubro",
        num_participantes=4,
    )
    capacitacion.save()
    capacitacion.creado_en = arrow.get(f"2022-{mes}-10T15:00:00+00:00").datetime
    capacitacion.save(update_fields=["creado_en"])
    participante_1 = Participante(
        nombre="Luis Correa",
        email="l.correa.bruna@gmail.com",
        rut="192140730",
        asiste=True,
        servicio=capacitacion,
    )
    participante_2 = Participante(
        nombre="Juan Robles",
        email="jurobles@gmail.com",
        rut="13338250K",
        asiste=True,
        servicio=capacitacion,
    )
    participante_3 = Participante(
        nombre="Luis Portilla",
        email="luportilla@gmail.com",
        rut="136530682",
        asiste=True,
        servicio=capacitacion,
    )
    participante_4 = Participante(
        nombre="Nicole Zamora",
        email="nicole.zamora@gmail.com",
        rut="172078834",
        asiste=True,
        servicio=capacitacion,
    )
    Participante.objects.bulk_create(
        [participante_1, participante_3, participante_2, participante_4]
    )

    # Actualizar factura Enero
    factura: FacturaMensual = FacturaMensual.objects.get(
        contrato__empresa_id=empresa_id, expiracion__month=int(mes)
    )
    factura.num_capacitaciones += 2
    factura.save()


def cargar_facturas_mensuales_para_empresa(empresa_id: int, mes: str):
    contrato = Contrato.objects.filter(empresa_id=empresa_id).first()
    # Factura Enero
    factura_mensual = FacturaMensual(
        expiracion=arrow.get(f"2022-{mes}-28T22:00:00+00:00")
        .replace(day=contrato.dia_facturacion)
        .datetime,
        contrato=contrato,
        total=contrato.valor_base,
        es_pagado=True,
        forma_pago="WEBPAY",
    )
    factura_mensual.save()
    factura_mensual.generado_en = arrow.get(f"2022-{mes}-01T00:00:00+00:00").datetime
    factura_mensual.save(update_fields=["generado_en"])


def cargar_factura_mensual_no_pagada_para_mes_actual(empresa_id):
    contrato = Contrato.objects.filter(empresa_id=empresa_id).first()
    # Factura Enero
    factura_mensual = FacturaMensual(
        expiracion=arrow.utcnow().replace(day=contrato.dia_facturacion).datetime,
        contrato=contrato,
        total=contrato.valor_base,
        es_pagado=False,
    )
    factura_mensual.save()
    factura_mensual.generado_en = arrow.utcnow().replace(day=1).datetime
    factura_mensual.save(update_fields=["generado_en"])


def cargar_asesorias_de_emergencia_para_empresa(empresa_id: int, mes: str):
    empresa = Empresa.objects.get(id=empresa_id)
    profesional = empresa.profesional_asignado
    # 1 Asesoria Emergencia 17/01/2022
    asesoria_emergencia = Servicio(
        tipo=TiposDeServicio.ASESORIA_EMERGENCIA,
        profesional=profesional,
        empresa=empresa,
        agendado_para=arrow.get(f"2022-{mes}-17T11:00:00+00:00").datetime,
        realizado_en=arrow.get(f"2022-{mes}-17T11:00:00+00:00").datetime,
        duracion=datetime.timedelta(
            hours=duracion_en_hrs_por_servicio[TiposDeServicio.ASESORIA_EMERGENCIA]
        ),
        motivo="Accidente en la sala de producción",
        contenido="2 trabajadores accidentados, se recomienda una fortificación en los aparatos y revisión semanal",
    )
    asesoria_emergencia.save()
    asesoria_emergencia.creado_en = arrow.get(f"2022-{mes}-17T10:00:00+00:00").datetime
    asesoria_emergencia.save(update_fields=["creado_en"])
    accidente = Evento(
        tipo="ACCIDENTE",
        fecha=arrow.get(f"2022-{mes}-17T09:00:00+00:00").datetime,
        contenido="ACCIDENTE LABORAL DE 2 TRABAJADORES",
        servicio=asesoria_emergencia,
    )
    accidente.save()

    # 2 Asesoria Emergencia 23/01/2022
    asesoria_emergencia = Servicio(
        tipo=TiposDeServicio.ASESORIA_EMERGENCIA,
        profesional=profesional,
        empresa=empresa,
        agendado_para=arrow.get(f"2022-{mes}-23T11:00:00+00:00").datetime,
        realizado_en=arrow.get(f"2022-{mes}-23T11:00:00+00:00").datetime,
        duracion=datetime.timedelta(
            hours=duracion_en_hrs_por_servicio[TiposDeServicio.ASESORIA_EMERGENCIA]
        ),
        motivo="Accidente en trabajo de campo",
        contenido="1 trabajador accidentado, se recomienda implementar nuevas herramientas para el tipo de trabajo",
    )
    asesoria_emergencia.save()
    asesoria_emergencia.creado_en = arrow.get(f"2022-{mes}-23T10:00:00+00:00").datetime
    asesoria_emergencia.save(update_fields=["creado_en"])
    accidente = Evento(
        tipo="ACCIDENTE",
        fecha=arrow.get(f"2022-{mes}-23T09:00:00+00:00").datetime,
        contenido="ACCIDENTE LABORAL DE 1 TRABAJADOR",
        servicio=asesoria_emergencia,
    )
    accidente.save()

    # Actualizar factura Enero
    factura: FacturaMensual = FacturaMensual.objects.get(
        contrato__empresa_id=empresa_id, expiracion__month=int(mes)
    )
    factura.num_asesorias += 2
    factura.save()


def cargar_asesorias_por_fiscalizacion_para_empresa(empresa_id: int, mes: str):
    empresa = Empresa.objects.get(id=empresa_id)
    profesional = empresa.profesional_asignado
    # 1. Asesoria 02/01/2022
    asesoria_fiscalizacion = Servicio(
        tipo=TiposDeServicio.ASESORIA_FISCALIZACION,
        profesional=profesional,
        empresa=empresa,
        agendado_para=arrow.get(f"2022-{mes}-02T16:00:00+00:00").datetime,
        realizado_en=arrow.get(f"2022-{mes}-02T16:00:00+00:00").datetime,
        duracion=datetime.timedelta(
            hours=duracion_en_hrs_por_servicio[TiposDeServicio.ASESORIA_FISCALIZACION]
        ),
        motivo="MULTA POR ENTIDAD FISCALIZADORA CORRESPONDIENTE A $100.000 POR NO USAR INDUMENTARIA ADECUADA",
        contenido="Se recomienda reevaluar la "
        "indumentaria utilizada para los trabajos "
        "y complementarla en caso de que haga falta",
    )
    asesoria_fiscalizacion.save()
    asesoria_fiscalizacion.creado_en = arrow.get(
        f"2022-{mes}-01T16:00:00+00:00"
    ).datetime
    asesoria_fiscalizacion.save(update_fields=["creado_en"])
    multa = Evento(
        tipo="MULTA",
        fecha=arrow.get(f"2022-{mes}-02T13:00:00+00:00").datetime,
        contenido="MULTA POR ENTIDAD FISCALIZADORA CORRESPONDIENTE A $100.000 POR NO USAR INDUMENTARIA ADECUADA",
        servicio=asesoria_fiscalizacion,
    )
    multa.save()

    # 2. Asesoria 10/01/2022
    asesoria_fiscalizacion = Servicio(
        tipo=TiposDeServicio.ASESORIA_FISCALIZACION,
        profesional=profesional,
        empresa=empresa,
        agendado_para=arrow.get(f"2022-{mes}-10T16:00:00+00:00").datetime,
        realizado_en=arrow.get(f"2022-{mes}-10T16:00:00+00:00").datetime,
        duracion=datetime.timedelta(
            hours=duracion_en_hrs_por_servicio[TiposDeServicio.ASESORIA_FISCALIZACION]
        ),
        motivo="MULTA POR ENTIDAD FISCALIZADORA CORRESPONDIENTE A $50.000 POR NO USAR IMPLEMENTOS DE SEGURIDAD",
        contenido="Se recomienda realizar un nuevo plan de los sistemas de seguridad y los implementos de la misma",
    )
    asesoria_fiscalizacion.save()
    asesoria_fiscalizacion.creado_en = arrow.get(
        f"2022-{mes}-09T16:00:00+00:00"
    ).datetime
    asesoria_fiscalizacion.save(update_fields=["creado_en"])
    multa = Evento(
        tipo="MULTA",
        fecha=arrow.get(f"2022-{mes}-09T13:00:00+00:00").datetime,
        contenido="MULTA POR ENTIDAD FISCALIZADORA CORRESPONDIENTE A $50.000 POR NO USAR IMPLEMENTOS DE SEGURIDAD",
        servicio=asesoria_fiscalizacion,
    )
    multa.save()

    # Actualizar factura Enero
    factura: FacturaMensual = FacturaMensual.objects.get(
        contrato__empresa_id=empresa_id, expiracion__month=int(mes)
    )
    factura.num_asesorias += 2
    factura.save()


def cargar_visitas_para_empresa(empresa_id: int, mes: str):
    empresa = Empresa.objects.get(id=empresa_id)
    profesional = empresa.profesional_asignado
    # 1. Visita Enero
    visita = Servicio(
        tipo=TiposDeServicio.VISITA,
        profesional=profesional,
        empresa=empresa,
        agendado_para=arrow.get(f"2022-{mes}-10T16:00:00+00:00").datetime,
        realizado_en=arrow.get(f"2022-{mes}-10T16:00:00+00:00").datetime,
        duracion=datetime.timedelta(
            hours=duracion_en_hrs_por_servicio[TiposDeServicio.VISITA]
        ),
        motivo="Visita pre-programada",
        contenido="Se recomienda invertir en mejorar la indumentaria de trabajo",
    )
    visita.save()
    # Actualizar factura Enero
    factura: FacturaMensual = FacturaMensual.objects.get(
        contrato__empresa_id=empresa_id, expiracion__month=int(mes)
    )
    factura.num_visitas += 1
    factura.save()


def cargar_llamadas_para_empresa(empresa_id: int, mes: str):
    empresa = Empresa.objects.get(id=empresa_id)
    profesional = empresa.profesional_asignado
    # 1. Llamada en horario
    llamada = Servicio(
        tipo=TiposDeServicio.LLAMADA,
        profesional=profesional,
        empresa=empresa,
        agendado_para=arrow.get(f"2022-{mes}-11T10:00:00+00:00").datetime,
        realizado_en=arrow.get(f"2022-{mes}-11T10:00:00+00:00").datetime,
        duracion=datetime.timedelta(minutes=30),
    )
    llamada.save()

    # 2. Llamada fuera de horario
    llamada = Servicio(
        tipo=TiposDeServicio.LLAMADA,
        profesional=profesional,
        empresa=empresa,
        agendado_para=arrow.get(f"2022-{mes}-10T00:10:00+00:00").datetime,
        realizado_en=arrow.get(f"2022-{mes}-10T00:10:00+00:00").datetime,
        duracion=datetime.timedelta(minutes=10),
    )
    llamada.save()
    # Actualizar factura mes
    factura: FacturaMensual = FacturaMensual.objects.get(
        contrato__empresa_id=empresa_id, expiracion__month=int(mes)
    )
    factura.num_llamadas += 1
    factura.num_llamadas_fuera_horario += 1
    factura.total += factura.valor_llamadas_fuera_horario
    factura.save()


def cargar_checklist_base(empresa_id: int):
    empresa = Empresa.objects.get(id=empresa_id)
    ChecklistBase.objects.create(
        items={
            "Cumple con las normas básicas de higiene": False,
            "Todos los trabajadores conocen el reglamento interno": False,
            "Todos los trabajadores usan el vestuario adecuado a sus labores": False,
        },
        empresa=empresa,
    )


def cargar_profesionales():
    datos_profesionales = [
        {
            "datos_user": dict(
                name="Luis Portilla",
                email="lu.portilla@duocuc.cl",
                username="lu.portilla",
                rut="250474474",
                password="250474474",
            ),
            "datos_profesional": dict(telefono=959998656),
        },
        {
            "datos_user": dict(
                name="Rosa Lara",
                email="ro.laral@duocuc.cl",
                username="ro.laral",
                rut="197612304",
                password="197612304",
            ),
            "datos_profesional": dict(telefono=959998650),
        },
        {
            "datos_user": dict(
                name="Gerald Vera",
                email="ge.vera@duocuc.cl",
                username="ge.vera",
                rut="204090874",
                password="204090874",
            ),
            "datos_profesional": dict(telefono=959118656),
        },
    ]
    grupo_profesional = Group.objects.get(name="profesional")
    for datos_profesional in datos_profesionales:
        password = datos_profesional["datos_user"].pop("password")

        usuario = User(**datos_profesional["datos_user"])
        usuario.password = make_password(password)
        usuario.save()

        usuario.groups.add(grupo_profesional)

        profesional = Profesional(
            usuario=usuario, **datos_profesional["datos_profesional"]
        )
        profesional.save()


def cargar_datos_empresa_y_usuarios():
    datos_clientes = [
        {
            "datos_user": dict(
                name="Juan Robles",
                email="ju.roblesb@duocuc.cl",
                username="ju.roblesb",
                rut="204186642",
                password="204186642",
            ),
            "datos_empresa": dict(
                rut="96928510",
                nombre="EMPRESAS LIPIGAS S.A.",
                giro="VENTA AL POR MENOR DE GAS LICUADO EN BOMBONAS (CILINDROS)",
                direccion="AV. APOQUINDO 5400 PISO 15",
                latitud=None,
                longitud=None,
                esta_activa=True,
                telefono=955347157,
                profesional_asignado_rut=250474474,
            ),
        },
        {
            "datos_user": dict(
                name="Alex Asenjo",
                email="al.asenjo@duocuc.cl",
                username="al.asenjo",
                rut="206235179",
                password="206235179",
            ),
            "datos_empresa": dict(
                rut="591569201",
                nombre="CODELCO S.A.",
                giro="VENTA AL POR MAYOR DE MINERALES",
                direccion="AV. SAN JOSE 532 PISO 10",
                latitud=None,
                longitud=None,
                esta_activa=True,
                telefono=955347000,
                profesional_asignado_rut=197612304,
            ),
        },
        {
            "datos_user": dict(
                name="Carlos Perez",
                email="ca.perez@duocuc.cl",
                username="ca.perez",
                rut="199767984",
                password="199767984",
            ),
            "datos_empresa": dict(
                rut="918060006",
                nombre="EMPRESAS ABASTIBLE S.A.",
                giro="VENTA AL POR MENOR DE GAS LICUADO EN BOMBONAS (CILINDROS)",
                direccion="AV. TORREALBA 53",
                latitud=None,
                longitud=None,
                esta_activa=True,
                telefono=955117157,
                profesional_asignado_rut=204090874,
            ),
        },
    ]
    grupo_cliente = Group.objects.get(name="cliente")
    for datos_cliente in datos_clientes:
        profesional_asignado_rut = datos_cliente["datos_empresa"].pop(
            "profesional_asignado_rut"
        )
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


class Command(BaseCommand):
    help = "Carga datos de prueba"

    def add_arguments(self, parser):
        pass
        # parser.add_argument('poll_ids', nargs='+', type=int)

    def handle(self, *args, **options):
        with transaction.atomic():
            cargar_profesionales()
            cargar_datos_empresa_y_usuarios()
            empresas = Empresa.objects.all()
            for empresa in empresas:
                # TODO: AGREGAR 11 EN DICIEMBRE
                cargar_factura_mensual_no_pagada_para_mes_actual(empresa_id=empresa.id)
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Cargando factura no pagada "
                        f"para mes actual para empresa id "
                        f"{empresa.id} - {empresa.nombre}"
                    )
                )
                cargar_checklist_base(empresa_id=empresa.id)
                self.stdout.write(
                    self.style.SUCCESS("ChecklistBase cargado satisfactoriamente")
                )

                for mes in ("09", "10"):
                    empresa_id = empresa.id
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"Cargando información para empresa id {empresa_id} - {empresa.nombre} y mes {mes}"
                        )
                    )
                    cargar_facturas_mensuales_para_empresa(
                        empresa_id=empresa_id, mes=mes
                    )
                    self.stdout.write(
                        self.style.SUCCESS("Factura mensual cargada satisfactoriamente")
                    )
                    cargar_capacitaciones_para_empresa(empresa_id=empresa_id, mes=mes)
                    self.stdout.write(
                        self.style.SUCCESS("Capacitaciones cargadas satisfactoriamente")
                    )
                    cargar_asesorias_de_emergencia_para_empresa(
                        empresa_id=empresa_id, mes=mes
                    )
                    self.stdout.write(
                        self.style.SUCCESS(
                            "Asesorias de emergencia cargadas satisfactoriamente"
                        )
                    )
                    cargar_asesorias_por_fiscalizacion_para_empresa(
                        empresa_id=empresa_id, mes=mes
                    )
                    self.stdout.write(
                        self.style.SUCCESS(
                            "Asesorias por fiscalizaciones cargadas satisfactoriamente"
                        )
                    )
                    cargar_visitas_para_empresa(empresa_id=empresa_id, mes=mes)
                    self.stdout.write(
                        self.style.SUCCESS("Visitas cargadas satisfactoriamente")
                    )
                    cargar_llamadas_para_empresa(empresa_id=empresa_id, mes=mes)
                    self.stdout.write(
                        self.style.SUCCESS("Llamadas cargadas satisfactoriamente")
                    )

                    actualizar_reporte_cliente(empresa_id=empresa_id)
                    self.stdout.write(
                        self.style.SUCCESS(
                            "Reporte de cliente actualizado satisfactoriamente"
                        )
                    )
                    self.stdout.write(
                        self.style.SUCCESS(
                            "Carga de datos finalizada satisfactoriamente"
                        )
                    )
