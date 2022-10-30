from django.urls import path

from no_mas_accidentes.clientes.views import (
    empresa_adeudada_view,
    home_view,
    realizar_pago_view,
    recepcion_transaccion_view,
    reporte_cliente_view,
    solicitar_asesoria_emergencia_view,
    transaccion_exitosa_view,
)

app_name = "clientes"
urlpatterns = [
    path("home/", view=home_view, name="home"),
    path("realizar-pago/", view=realizar_pago_view, name="realizar_pago"),
    path("empresa-adeudada/", view=empresa_adeudada_view, name="empresa_adeudada"),
    path(
        "transaccion-exitosa/",
        view=transaccion_exitosa_view,
        name="transaccion_exitosa",
    ),
    path(
        "recepcion-transaccion/",
        view=recepcion_transaccion_view,
        name="recepcion_transaccion",
    ),
    path("reporte-historico/", view=reporte_cliente_view, name="reporte_cliente"),
    path(
        "solicitar-asesoria-emergencia/",
        view=solicitar_asesoria_emergencia_view,
        name="solicitar_asesoria_emergencia",
    ),
]
