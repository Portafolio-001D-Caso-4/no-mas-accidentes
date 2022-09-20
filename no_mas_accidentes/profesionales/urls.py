from django.urls import path

from no_mas_accidentes.profesionales.views import (
    home_view,
    lista_empresas_asignadas_view,
)

app_name = "profesionales"
urlpatterns = [
    path("home/", view=home_view, name="home"),
    path(
        "mantenedor-empresas/lista",
        view=lista_empresas_asignadas_view,
        name="empresas_asignadas_lista",
    ),
]
