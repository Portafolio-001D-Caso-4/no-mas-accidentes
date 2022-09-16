import datetime

import arrow
from django.core.management.base import BaseCommand

from no_mas_accidentes.clientes.models import Empresa, FacturaMensual
from no_mas_accidentes.profesionales.models import Profesional
from no_mas_accidentes.servicios.constants import (
    TiposDeServicio,
    duracion_en_hrs_por_servicio,
)
from no_mas_accidentes.servicios.models import Servicio


def cargar_info_prueba_servicios():
    empresa = Empresa.objects.first()
    profesional = Profesional.objects.first()
    capacitacion = Servicio(
        tipo=TiposDeServicio.CAPACITACION,
        profesional=profesional,
        empresa=empresa,
        agendado_para=arrow.get("2022-09-15T15:00:00+00:00").datetime,
        realizado_en=arrow.get("2022-09-15T15:00:00+00:00").datetime,
        duracion=datetime.timedelta(
            hours=duracion_en_hrs_por_servicio[TiposDeServicio.CAPACITACION]
        ),
    )
    asesoria_emergencia = Servicio(
        tipo=TiposDeServicio.ASESORIA_EMERGENCIA,
        profesional=profesional,
        empresa=empresa,
        agendado_para=arrow.get("2022-09-20T16:00:00+00:00").datetime,
        realizado_en=None,
        duracion=datetime.timedelta(
            hours=duracion_en_hrs_por_servicio[TiposDeServicio.ASESORIA_EMERGENCIA]
        ),
    )
    asesoria_fiscalizacion = Servicio(
        tipo=TiposDeServicio.ASESORIA_FISCALIZACION,
        profesional=profesional,
        empresa=empresa,
        agendado_para=arrow.get("2022-09-22T16:00:00+00:00").datetime,
        realizado_en=None,
        duracion=datetime.timedelta(
            hours=duracion_en_hrs_por_servicio[TiposDeServicio.ASESORIA_FISCALIZACION]
        ),
    )
    Servicio.objects.bulk_create(
        [capacitacion, asesoria_emergencia, asesoria_fiscalizacion]
    )

    factura_mensual = FacturaMensual.objects.first()
    factura_mensual.num_capacitaciones = factura_mensual.num_capacitaciones + 1
    factura_mensual.num_asesorias = factura_mensual.num_asesorias + 2
    factura_mensual.save()


class Command(BaseCommand):
    help = "Carga datos de prueba"

    def add_arguments(self, parser):
        pass
        # parser.add_argument('poll_ids', nargs='+', type=int)

    def handle(self, *args, **options):
        cargar_info_prueba_servicios()
        self.stdout.write(self.style.SUCCESS("Información cargada satisfactoriamente"))
