from django.urls import path

from no_mas_accidentes.administracion.views import (
    actualizar_reporte_cliente_view,
    crear_cliente_view,
    crear_empresa_view,
    crear_profesional_view,
    descarga_contrato_base_view,
    detalle_cliente_informacion_view,
    detalle_empresa_contrato_view,
    detalle_empresa_contratos_view,
    detalle_empresa_informacion_view,
    detalle_empresa_pago_view,
    detalle_empresa_pagos_view,
    detalle_profesional_informacion_view,
    enviar_recordatorio_no_pago_view,
    home_view,
    lista_clientes_view,
    lista_empresas_view,
    lista_profesionales_view,
    lista_servicios_view,
    reporte_global_view,
)

app_name = "administracion"
urlpatterns = [
    path("home/", view=home_view, name="home"),
    path(
        "mantenedor-clientes/lista",
        view=lista_clientes_view,
        name="mantenedor_clientes_lista",
    ),
    path(
        "mantenedor-clientes/crear",
        view=crear_cliente_view,
        name="mantenedor_clientes_crear",
    ),
    path(
        "mantenedor-clientes/<int:pk>/informacion",
        view=detalle_cliente_informacion_view,
        name="mantenedor_clientes_detalle_informacion",
    ),
    path(
        "mantenedor-profesionales/lista",
        view=lista_profesionales_view,
        name="mantenedor_profesionales_lista",
    ),
    path(
        "mantenedor-profesionales/crear",
        view=crear_profesional_view,
        name="mantenedor_profesionales_crear",
    ),
    path(
        "mantenedor-profesionales/<int:pk>/informacion",
        view=detalle_profesional_informacion_view,
        name="mantenedor_profesionales_detalle_informacion",
    ),
    path(
        "mantenedor-empresas/lista",
        view=lista_empresas_view,
        name="mantenedor_empresas_lista",
    ),
    path(
        "mantenedor-empresas/crear",
        view=crear_empresa_view,
        name="mantenedor_empresas_crear",
    ),
    path(
        "mantenedor-empresas/<int:pk>/informacion",
        view=detalle_empresa_informacion_view,
        name="mantenedor_empresas_detalle_informacion",
    ),
    path(
        "mantenedor-empresas/<int:pk>/contratos",
        view=detalle_empresa_contratos_view,
        name="mantenedor_empresas_detalle_contratos",
    ),
    path(
        "mantenedor-empresas/<int:pk>/contrato/<int:contrato_id>",
        view=detalle_empresa_contrato_view,
        name="mantenedor_empresas_detalle_contrato",
    ),
    path(
        "mantenedor-empresas/<int:pk>/pagos",
        view=detalle_empresa_pagos_view,
        name="mantenedor_empresas_detalle_pagos",
    ),
    path(
        "mantenedor-empresas/<int:pk>/pagos/<int:factura_mensual_id>",
        view=detalle_empresa_pago_view,
        name="mantenedor_empresas_detalle_pago",
    ),
    path(
        "servicios/lista",
        view=lista_servicios_view,
        name="servicios_lista",
    ),
    path(
        "contratos/<int:pk>/descarga_base",
        view=descarga_contrato_base_view,
        name="descarga_contrato_base_pdf",
    ),
    path(
        "contratos/<int:pk>/enviar-recordatorio-no-pago/<int:factura_mensual_id>",
        view=enviar_recordatorio_no_pago_view,
        name="enviar_recordatorio_no_pago",
    ),
    path("reporte-global/", view=reporte_global_view, name="reporte_global"),
    path(
        "mantenedor-empresas/<int:pk>/modificar-reporte/",
        view=actualizar_reporte_cliente_view,
        name="actualizar_reporte_cliente",
    ),
]
