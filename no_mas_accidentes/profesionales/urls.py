from django.urls import path

from no_mas_accidentes.profesionales.views import (
    detalle_empresa_informacion_view,
    home_view,
    lista_empresas_asignadas_view,
)

app_name = "profesionales"
urlpatterns = [
    path("home/", view=home_view, name="home"),
    path(
        "empresas-asignadas/lista",
        view=lista_empresas_asignadas_view,
        name="empresas_asignadas_lista",
    ),
    path(
        "empresas-asignadas/<int:pk>/informacion",
        view=detalle_empresa_informacion_view,
        name="empresas_asignadas_detalle_informacion",
    ),
]
