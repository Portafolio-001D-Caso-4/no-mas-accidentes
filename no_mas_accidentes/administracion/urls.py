from django.urls import path

from no_mas_accidentes.administracion.views import (
    crear_cliente_view,
    home_view,
    lista_clientes_view,
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
]
