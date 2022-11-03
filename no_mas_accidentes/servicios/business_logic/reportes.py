import arrow
import redis

from no_mas_accidentes.servicios.models import Servicio


def actualizar_reporte_cliente(empresa_id: int):
    redis_storage = redis.Redis.from_url(
        url="redis://redis:6379/0",
    )

    redis_storage.set(
        f"reporte_cliente_empresa_{empresa_id}",
        arrow.utcnow().int_timestamp,
        ex=9999999999,
    )


def traer_informacion_reporte_cliente(empresa_id: int):
    redis_storage = redis.Redis.from_url(
        url="redis://redis:6379/0",
    )
    timestamp = redis_storage.get(f"reporte_cliente_empresa_{empresa_id}")
    if timestamp:
        hasta = arrow.get(int(timestamp.decode("utf-8"))).to("UTC").datetime
    else:
        hasta = arrow.utcnow().datetime
    return (
        Servicio.objects.filter(realizado_en__lte=hasta, empresa_id=empresa_id)
        .prefetch_related("oportunidaddemejora_set", "evento_set")
        .select_related("checklist")
        .order_by("realizado_en", "tipo"),
        hasta,
    )
