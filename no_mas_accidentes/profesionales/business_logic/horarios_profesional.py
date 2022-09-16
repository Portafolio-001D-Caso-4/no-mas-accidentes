import datetime

import arrow
from django.db.models import DateTimeField, ExpressionWrapper, F

from no_mas_accidentes.profesionales.constants import HORAS_NECESARIAS_ANTES_DE_AGENDAR
from no_mas_accidentes.profesionales.models import HorarioProfesional
from no_mas_accidentes.utils import fechas


def pairwise(iterable):
    it = iter(iterable)
    a = next(it, None)

    for b in it:
        yield (a, b)
        a = b


def generar_horario_profesional(
    id_profesional: int,
    dias_buscados: tuple[int, ...],
    cantidad_de_semanas: int,
    dia_inicio: datetime.date,
    desde: int,
    hasta: int,
) -> list[HorarioProfesional]:
    dia_fin = dia_inicio + datetime.timedelta(weeks=cantidad_de_semanas)

    dias_trabajados_en_semana = fechas.traer_dias_especificos_entre_fechas(
        inicio=dia_inicio, fin=dia_fin, dias_buscados=dias_buscados
    )
    horas = list(range(desde, hasta + 1))
    horas_desde_hasta = list(pairwise(horas))
    horarios = []
    for dia in dias_trabajados_en_semana:
        for desde, hasta in horas_desde_hasta:
            horarios.append(
                HorarioProfesional(
                    fecha_inicio=dia,
                    fecha_termino=dia,
                    desde=datetime.time(desde),
                    hasta=datetime.time(hasta),
                    profesional_id=id_profesional,
                )
            )
    return horarios


def traer_horarios_futuros_de_profesional(
    id_profesional: int,
) -> list[HorarioProfesional]:
    dia_actual = arrow.utcnow().shift(hours=+HORAS_NECESARIAS_ANTES_DE_AGENDAR).datetime
    horarios = (
        HorarioProfesional.objects.all()
        .annotate(
            fecha_inicio_desde=ExpressionWrapper(
                F("fecha_inicio") + F("desde"), output_field=DateTimeField()
            )
        )
        .filter(profesional_id=id_profesional, fecha_inicio_desde__gte=dia_actual)
    )
    return list(horarios)
