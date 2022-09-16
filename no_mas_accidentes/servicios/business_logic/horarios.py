import datetime

import arrow

from no_mas_accidentes.profesionales.business_logic import horarios_profesional
from no_mas_accidentes.profesionales.models import HorarioProfesional
from no_mas_accidentes.servicios.models import Servicio


def traer_horarios_disponibles_de_profesional(
    id_profesional: int,
) -> list[HorarioProfesional]:
    fecha_actual = arrow.utcnow().datetime
    horarios_ocupados = list(
        Servicio.objects.filter(
            profesional_id=id_profesional, agendado_para__gte=fecha_actual
        )
    )
    horarios_futuros = horarios_profesional.traer_horarios_futuros_de_profesional(
        id_profesional=id_profesional
    )
    horarios_disponibles = []
    for horario_futuro in horarios_futuros:
        esta_ocupado = False
        horario_desde = (
            arrow.get(
                datetime.datetime.combine(
                    date=horario_futuro.fecha_inicio, time=horario_futuro.desde
                )
            )
            .to("UTC")
            .datetime
        )
        horario_hasta = (
            arrow.get(
                datetime.datetime.combine(
                    date=horario_futuro.fecha_termino, time=horario_futuro.hasta
                )
            )
            .to("UTC")
            .datetime
        )
        for horario_ocupado in horarios_ocupados:
            if (
                horario_desde < horario_ocupado.agendado_para + horario_ocupado.duracion
                and horario_ocupado.agendado_para < horario_hasta
            ):
                esta_ocupado = True
                break
        if not esta_ocupado:
            horarios_disponibles.append(horario_futuro)
    return horarios_disponibles
