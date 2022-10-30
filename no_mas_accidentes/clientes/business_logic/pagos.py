from no_mas_accidentes.clientes.models import FacturaMensual
from no_mas_accidentes.clientes.tasks import enviar_alerta_pago_realizado
from no_mas_accidentes.users.models import User


def realizar_pago_ultima_factura(id_cliente: int):
    usuario = User.objects.get(id=id_cliente)
    empresa_id = usuario.empresa_id
    factura_actual = FacturaMensual.objects.filter(
        contrato__empresa_id=empresa_id, es_pagado=False
    ).last()
    factura_actual.forma_pago = "WEBPAY"
    factura_actual.pagado_por = usuario
    factura_actual.es_pagado = True
    factura_actual.save()
    enviar_alerta_pago_realizado.delay(
        usuario_id=usuario.id, empresa_id=empresa_id, factura_id=factura_actual.id
    )
