import arrow
from django.db.models.aggregates import Count

from no_mas_accidentes.servicios.constants import TiposDeServicio
from no_mas_accidentes.servicios.models import Servicio


def calcular_accidentabilidad_por_profesional(
    profesional_id: int, historico: bool = False
) -> float:
    mes_actual = arrow.utcnow().datetime.month
    queryset = Servicio.objects.filter(profesional__usuario__pk=profesional_id)
    if historico is False:
        queryset = queryset.filter(realizado_en__month=mes_actual)
    cantidad_servicios_por_tipo = list(
        queryset.values("tipo").order_by("tipo").annotate(count=Count("tipo"))
    )
    cantidad_total_servicios = sum(
        cantidad_servicios_por_tipo["count"]
        for cantidad_servicios_por_tipo in cantidad_servicios_por_tipo
        if cantidad_servicios_por_tipo["tipo"]
        in (TiposDeServicio.ASESORIA_EMERGENCIA, TiposDeServicio.ASESORIA_FISCALIZACION)
    )
    cantidad_de_accidentes = sum(
        cantidad_servicios_por_tipo["count"]
        for cantidad_servicios_por_tipo in cantidad_servicios_por_tipo
        if cantidad_servicios_por_tipo["tipo"] == TiposDeServicio.ASESORIA_EMERGENCIA
    )
    if cantidad_total_servicios == 0:
        return 0
    return round(cantidad_de_accidentes * 100 / cantidad_total_servicios, 2)
