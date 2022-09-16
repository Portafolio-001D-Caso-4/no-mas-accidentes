from typing import Any

from django.db.models import QuerySet

from no_mas_accidentes.servicios.constants import TiposDeServicio
from no_mas_accidentes.servicios.models import Servicio


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
            "url": "#",
            "profesional_asignado": servicio.profesional.usuario.name,
            "empresa": servicio.empresa.nombre,
        }
        for servicio in servicios
    ]
