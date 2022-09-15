import calendar
import datetime

from no_mas_accidentes.utils import fechas


def test_traer_fechas_entre():
    inicio = datetime.date(2022, 9, 12)
    fin = datetime.date(2022, 9, 15)

    resultados = list(fechas.traer_fechas_entre(inicio=inicio, fin=fin))

    assert resultados == [
        datetime.date(2022, 9, 12),
        datetime.date(2022, 9, 13),
        datetime.date(2022, 9, 14),
        datetime.date(2022, 9, 15),
    ]


def test_traer_dias_especificos_entre_fechas():
    inicio = datetime.date(2022, 9, 12)
    fin = datetime.date(2022, 9, 30)
    dias_buscados = (calendar.MONDAY, calendar.FRIDAY)
    resultados = list(
        fechas.traer_dias_especificos_entre_fechas(
            inicio=inicio, fin=fin, dias_buscados=dias_buscados
        )
    )

    assert resultados == [
        datetime.date(2022, 9, 12),
        datetime.date(2022, 9, 16),
        datetime.date(2022, 9, 19),
        datetime.date(2022, 9, 23),
        datetime.date(2022, 9, 26),
        datetime.date(2022, 9, 30),
    ]
