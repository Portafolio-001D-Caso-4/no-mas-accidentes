from django.urls import path

from no_mas_accidentes.profesionales.views import (
    actualizar_actividad_de_mejora_view,
    actualizar_asesoria_emergencia_view,
    actualizar_asistencia_capacitacion_view,
    actualizar_capacitacion_view,
    actualizar_checklist_view,
    actualizar_visita_view,
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
    path(
        "capacitacion/<int:pk>/actualizar",
        view=actualizar_capacitacion_view,
        name="capacitacion_actualizar",
    ),
    path(
        "capacitacion/<int:pk>/asistencia",
        view=actualizar_asistencia_capacitacion_view,
        name="capacitacion_actualizar_asistencia",
    ),
    path(
        "visita/<int:pk>/actualizar",
        view=actualizar_visita_view,
        name="visita_actualizar",
    ),
    path(
        "visita/<int:pk>/checklist",
        view=actualizar_checklist_view,
        name="visita_actualizar_checklist",
    ),
    path(
        "visita/<int:pk>/actividad-de-mejora",
        view=actualizar_actividad_de_mejora_view,
        name="visita_actualizar_actividad_mejora",
    ),
]
