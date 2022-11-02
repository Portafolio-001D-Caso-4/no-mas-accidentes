import datetime
from typing import Any

import arrow
from django.core.exceptions import ValidationError
from django.db.models import QuerySet
from django.urls import reverse

from no_mas_accidentes.clientes.models import Empresa, FacturaMensual
from no_mas_accidentes.servicios.business_logic.horarios import (
    traer_horarios_disponibles_de_profesional,
)
from no_mas_accidentes.servicios.constants import (
    TiposDeServicio,
    duracion_en_hrs_por_servicio,
)
from no_mas_accidentes.servicios.models import Evento, Servicio
from no_mas_accidentes.users.models import User


def traer_servicios_por_empresa(id_empresa: int) -> QuerySet[Servicio]:
    return Servicio.objects.filter(empresa_id=id_empresa).exclude(
        tipo=TiposDeServicio.LLAMADA
    )


def traer_context_data_de_servicios_por_empresa(
    id_empresa: int,
) -> list[dict[str, Any]]:
    servicios = traer_servicios_por_empresa(id_empresa=id_empresa)
    return [
        {
            "title": servicio.tipo,
            "month": servicio.agendado_para.month,
            "day": servicio.agendado_para.day,
            "year": servicio.agendado_para.year,
            "start_hour": servicio.agendado_para.hour,
            "start_min": servicio.agendado_para.minute,
            "start_second": servicio.agendado_para.second,
            "end_hour": (servicio.agendado_para + servicio.duracion).hour,
            "end_min": (servicio.agendado_para + servicio.duracion).minute,
            "end_second": (servicio.agendado_para + servicio.duracion).second,
            "all_day": False,
            "class_name": "bg-warning",
            "url": get_url_empresa_por_servicio(servicio=servicio),
            "profesional_asignado": servicio.profesional.usuario.name,
            "empresa": servicio.empresa.nombre,
        }
        for servicio in servicios
    ]


def get_url_empresa_por_servicio(servicio: Servicio) -> str:
    # if servicio.tipo == TiposDeServicio.VISITA:
    #     return reverse("profesionales:visita_actualizar", kwargs={"pk": servicio.pk})
    # if servicio.tipo == TiposDeServicio.CAPACITACION:
    #     return reverse("profesionales:capacitacion_actualizar", kwargs={"pk": servicio.pk})
    # if servicio.tipo == TiposDeServicio.ASESORIA_EMERGENCIA:
    #     return reverse("profesionales:asesoria_emergencia_actualizar", kwargs={"pk": servicio.pk})
    # if servicio.tipo == TiposDeServicio.ASESORIA_FISCALIZACION:
    #     return reverse("profesionales:asesoria_actualizar", kwargs={"pk": servicio.pk})
    return "#"


def traer_servicios_por_profesional(id_profesional: int) -> QuerySet[Servicio]:
    return Servicio.objects.filter(profesional_id=id_profesional).exclude(
        tipo=TiposDeServicio.LLAMADA
    )


def traer_context_data_de_servicios_por_profesional(
    id_profesional: int,
) -> list[dict[str, Any]]:
    servicios = traer_servicios_por_profesional(id_profesional=id_profesional)
    return [
        {
            "title": servicio.tipo,
            "month": servicio.agendado_para.month,
            "day": servicio.agendado_para.day,
            "year": servicio.agendado_para.year,
            "start_hour": servicio.agendado_para.hour,
            "start_min": servicio.agendado_para.minute,
            "start_second": servicio.agendado_para.second,
            "end_hour": (servicio.agendado_para + servicio.duracion).hour,
            "end_min": (servicio.agendado_para + servicio.duracion).minute,
            "end_second": (servicio.agendado_para + servicio.duracion).second,
            "all_day": False,
            "class_name": "bg-warning",
            "url": get_url_profesional_por_servicio(servicio=servicio),
            "profesional_asignado": servicio.profesional.usuario.name,
            "empresa": servicio.empresa.nombre,
        }
        for servicio in servicios
    ]


def get_url_profesional_por_servicio(servicio: Servicio) -> str:
    if servicio.tipo == TiposDeServicio.VISITA:
        return reverse("profesionales:visita_actualizar", kwargs={"pk": servicio.pk})
    if servicio.tipo == TiposDeServicio.CAPACITACION:
        return reverse(
            "profesionales:capacitacion_actualizar", kwargs={"pk": servicio.pk}
        )
    if servicio.tipo == TiposDeServicio.ASESORIA_EMERGENCIA:
        return reverse(
            "profesionales:asesoria_emergencia_actualizar", kwargs={"pk": servicio.pk}
        )
    if servicio.tipo == TiposDeServicio.ASESORIA_FISCALIZACION:
        return reverse("profesionales:asesoria_actualizar", kwargs={"pk": servicio.pk})
    return "#"


def crear_asesoria_de_emergencia_para_empresa(
    id_empresa: int, solicitante: User, accidente: Evento, enviar_alerta_accidente=None
):
    empresa = Empresa.objects.get(id=id_empresa)
    try:
        horario_a_escoger = traer_horarios_disponibles_de_profesional(
            id_profesional=empresa.profesional_asignado_id
        )[0]
    except IndexError:
        raise ValidationError("El profesional asignado no tiene horarios disponibles")
    servicio = Servicio(
        tipo=TiposDeServicio.ASESORIA_EMERGENCIA,
        profesional_id=empresa.profesional_asignado_id,
        empresa_id=empresa.id,
        agendado_para=arrow.get(
            datetime.datetime.combine(
                date=horario_a_escoger.fecha_inicio,
                time=horario_a_escoger.desde,
            )
        )
        .to("UTC")
        .datetime,
        duracion=datetime.timedelta(
            hours=duracion_en_hrs_por_servicio[TiposDeServicio.ASESORIA_EMERGENCIA]
        ),
    )
    servicio.save()
    accidente.servicio = servicio
    accidente.save()

    factura_mensual = FacturaMensual.objects.filter(contrato__empresa=empresa).last()
    factura_mensual.agregar_nueva_asesoria(
        asesoria=servicio, generado_por=solicitante.id
    )
    # enviar_alerta_accidente.delay(id_evento=accidente.id)
