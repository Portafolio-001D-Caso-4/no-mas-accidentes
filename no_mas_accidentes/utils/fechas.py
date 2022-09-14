import datetime
from collections.abc import Generator


def traer_fechas_entre(
    inicio: datetime.date, fin: datetime.date, minutos=60 * 24
) -> Generator[datetime.date, None, None]:
    fecha = inicio
    while fecha <= fin:
        yield fecha
        fecha += datetime.timedelta(minutes=minutos)


def traer_dias_especificos_entre_fechas(
    inicio: datetime.date, fin: datetime.date, dias_buscados: tuple[int, ...]
) -> list[datetime.date]:
    rango_fechas = traer_fechas_entre(inicio, fin)
    return [d for d in rango_fechas if d.weekday() in dias_buscados]
