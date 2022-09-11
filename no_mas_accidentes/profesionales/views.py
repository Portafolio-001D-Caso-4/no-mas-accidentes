from django.views.generic import TemplateView

from no_mas_accidentes.profesionales.constants import app_name
from no_mas_accidentes.profesionales.mixins import EsProfesionalMixin


class Home(EsProfesionalMixin, TemplateView):
    template_name = f"{app_name}/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["num_visitas"] = 1
        context["num_capacitaciones"] = 2
        context["num_asesorias"] = 3
        context["num_llamadas"] = 4

        context["num_accidentes"] = 1
        context["num_multas"] = 1
        context["porcentaje_accidentabilidad"] = 10

        agendas = [
            {
                "title": "Capacitación 1",
                "month": 9,
                "day": 22,
                "year": 2022,
                "start_hour": 10,
                "start_min": 0,
                "start_second": 0,
                "end_hour": 11,
                "end_min": 0,
                "end_second": 0,
                "all_day": False,
                "class_name": "bg-warning",
                "url": "#",
                "profesional_asignado": "Luis Portilla",
                "empresa": "Gasco S.A.",
            },
            {
                "title": "Capacitación 2",
                "month": 12,
                "day": 15,
                "year": 2022,
                "start_hour": 10,
                "start_min": 0,
                "start_second": 0,
                "end_hour": 11,
                "end_min": 0,
                "end_second": 0,
                "all_day": False,
                "class_name": "bg-warning",
                "url": "#",
                "profesional_asignado": "Luis Portilla",
                "empresa": "Gasco S.A.",
            },
        ]
        context["agendas"] = agendas
        return context


home_view = Home.as_view()
