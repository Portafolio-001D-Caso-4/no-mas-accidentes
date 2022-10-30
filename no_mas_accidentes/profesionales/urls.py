from django.urls import path

from no_mas_accidentes.profesionales.views import (
    actualizar_asesoria_emergencia_view,
    crear_o_actualizar_checklist_base_view,
    detalle_empresa_informacion_view,
    home_view,
    lista_empresas_asignadas_view,
    lista_servicios_asignados_view,
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
    path(
        "empresas-asignadas/<int:pk>/checklist_base/",
        view=crear_o_actualizar_checklist_base_view,
        name="empresas_asignadas_crear_o_actualizar_checklist_base",
    ),
    path(
        "servicios/lista",
        view=lista_servicios_asignados_view,
        name="servicios_asignados_lista",
    ),
    path(
        "asesoria-emergencia/<int:pk>/actualizar",
        view=actualizar_asesoria_emergencia_view,
        name="asesoria_emergencia_actualizar",
    ),
]
