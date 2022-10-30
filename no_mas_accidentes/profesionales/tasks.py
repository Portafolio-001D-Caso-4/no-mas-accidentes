import logging

import arrow

from config import celery_app
from no_mas_accidentes.profesionales.business_logic import horarios_profesional
from no_mas_accidentes.profesionales.models import HorarioProfesional, Profesional

logger = logging.getLogger(__name__)


@celery_app.task()
def crear_periodicamente_horarios_profesionales():
    profesionales = Profesional.objects.all()
    horarios = []
    for profesional in profesionales:
        # dias_buscados = (
        #     range(calendar.MONDAY, calendar.SATURDAY)
        #     if profesional.pk % 2 == 0
        #     else range(calendar.WEDNESDAY, calendar.FRIDAY)
        # )
        # desde, hasta = (10, 16) if profesional.pk % 2 == 0 else (16, 20)
        cantidad_de_semanas = 2 if profesional.pk % 2 == 0 else 1
        dias_buscados = (0, 1, 2, 3, 4, 5, 6)
        desde, hasta = (1, 23)
        horarios.extend(
            horarios_profesional.generar_horario_profesional(
                id_profesional=profesional.pk,
                dias_buscados=(tuple(list(dias_buscados))),
                cantidad_de_semanas=cantidad_de_semanas,
                dia_inicio=arrow.utcnow().shift(days=-1).date(),
                desde=desde,
                hasta=hasta,
            )
        )
    HorarioProfesional.objects.bulk_create(horarios, ignore_conflicts=True)
