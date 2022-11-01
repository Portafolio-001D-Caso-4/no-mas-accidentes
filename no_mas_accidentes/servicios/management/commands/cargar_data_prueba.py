import datetime

import arrow
from django.core.management.base import BaseCommand

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


def cargar_capacitaciones_para_empresa(empresa_id: int, mes: str):
    empresa = Empresa.objects.get(id=empresa_id)
    profesional = Profesional.objects.first()

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
        email="luportilla@gmail.com",
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
        expiracion=arrow.get(f"2022-{mes}-10T22:00:00+00:00")
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


def cargar_asesorias_de_emergencia_para_empresa(empresa_id: int, mes: str):
    empresa = Empresa.objects.get(id=empresa_id)
    profesional = Profesional.objects.first()
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
    )
    asesoria_emergencia.save()
    asesoria_emergencia.creado_en = arrow.get(f"2022-{mes}-17T10:00:00+00:00").datetime
    asesoria_emergencia.save(update_fields=["creado_en"])
    accidente = Evento(
        tipo="ACCIDENTE",
        fecha=arrow.get(f"2022-{mes}-17T09:00:00+00:00").datetime,
        contenido="ACCIDENTE LABORAL DE 3 TRABAJADORES",
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
    )
    asesoria_emergencia.save()
    asesoria_emergencia.creado_en = arrow.get(f"2022-{mes}-23T10:00:00+00:00").datetime
    asesoria_emergencia.save(update_fields=["creado_en"])
    accidente = Evento(
        tipo="ACCIDENTE",
        fecha=arrow.get(f"2022-{mes}-23T09:00:00+00:00").datetime,
        contenido="ACCIDENTE LABORAL DE 10 TRABAJADORES",
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
    profesional = Profesional.objects.first()
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
    profesional = Profesional.objects.first()
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
    profesional = Profesional.objects.first()
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
    # Actualizar factura Enero
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


class Command(BaseCommand):
    help = "Carga datos de prueba"

    def add_arguments(self, parser):
        pass
        # parser.add_argument('poll_ids', nargs='+', type=int)

    def handle(self, *args, **options):
        empresa_id = Empresa.objects.first().id
        mes = "03"
        self.stdout.write(
            self.style.SUCCESS(
                f"Cargando información para empresa id {empresa_id} y mes {mes}"
            )
        )
        cargar_facturas_mensuales_para_empresa(empresa_id=empresa_id, mes=mes)
        self.stdout.write(
            self.style.SUCCESS("Factura mensual cargada satisfactoriamente")
        )
        cargar_capacitaciones_para_empresa(empresa_id=empresa_id, mes=mes)
        self.stdout.write(
            self.style.SUCCESS("Capacitaciones cargadas satisfactoriamente")
        )
        cargar_asesorias_de_emergencia_para_empresa(empresa_id=empresa_id, mes=mes)
        self.stdout.write(
            self.style.SUCCESS("Asesorias de emergencia cargadas satisfactoriamente")
        )
        cargar_asesorias_por_fiscalizacion_para_empresa(empresa_id=empresa_id, mes=mes)
        self.stdout.write(
            self.style.SUCCESS(
                "Asesorias por fiscalizaciones cargadas satisfactoriamente"
            )
        )
        cargar_visitas_para_empresa(empresa_id=empresa_id, mes=mes)
        self.stdout.write(self.style.SUCCESS("Visitas cargadas satisfactoriamente"))
        cargar_llamadas_para_empresa(empresa_id=empresa_id, mes=mes)
        self.stdout.write(self.style.SUCCESS("Llamadas cargadas satisfactoriamente"))
        cargar_checklist_base(empresa_id=empresa_id)
        self.stdout.write(
            self.style.SUCCESS("ChecklistBase cargado satisfactoriamente")
        )
        actualizar_reporte_cliente(empresa_id=empresa_id)
        self.stdout.write(
            self.style.SUCCESS("Reporte de cliente actualizado satisfactoriamente")
        )
        self.stdout.write(
            self.style.SUCCESS("Carga de datos finalizada satisfactoriamente")
        )
