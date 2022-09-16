import calendar
import datetime

import pytest
from pytz import UTC

from no_mas_accidentes.profesionales.business_logic.horarios_profesional import (
    generar_horario_profesional,
)
from no_mas_accidentes.profesionales.models import HorarioProfesional, Profesional
from no_mas_accidentes.servicios.business_logic.horarios import (
    traer_horarios_disponibles_de_profesional,
)
from no_mas_accidentes.servicios.models import Servicio


@pytest.mark.freeze_time("2022-9-15", tz_offset=0)
def test_traer_horarios_disponibles_de_profesional(usuario_profesional):
    profesional = Profesional.objects.get(usuario=usuario_profesional)
    horarios_profesional = generar_horario_profesional(
        id_profesional=profesional.pk,
        dias_buscados=(calendar.MONDAY, calendar.TUESDAY),
        cantidad_de_semanas=1,
        dia_inicio=datetime.datetime.utcnow(),
        desde=10,
        hasta=16,
    )
    horarios_profesional = HorarioProfesional.objects.bulk_create(horarios_profesional)
    # dias 19 y 20
    # Horarios del empleado
    # 10:00 - 11:00         - ocupado CAPACITACION de 10:00 a 12:00
    # 11:00 - 12:00         - ocupado CAPACITACION de 10:00 a 12:00
    # 12:00 - 13:00
    # 13:00 - 14:00
    # 14:00 - 15:00         - ocupado visita de 14:00 a 15:00
    # 15:00 - 16:00

    assert len(horarios_profesional) == 12

    Servicio(
        tipo="CAPACITACION",
        profesional_id=profesional.pk,
        agendado_para=datetime.datetime(2022, 9, 19, 10, 0, tzinfo=UTC),
        duracion=datetime.timedelta(hours=2),
    ).save()
    Servicio(
        tipo="VISITA",
        profesional_id=profesional.pk,
        agendado_para=datetime.datetime(2022, 9, 19, 14, 0, tzinfo=UTC),
        duracion=datetime.timedelta(hours=1),
    ).save()

    resultados = traer_horarios_disponibles_de_profesional(
        id_profesional=profesional.pk
    )

    assert len(resultados) == 9
