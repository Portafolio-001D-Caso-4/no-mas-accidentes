from django.views.generic import TemplateView

from no_mas_accidentes.profesionales.constants import app_name
from no_mas_accidentes.profesionales.mixins import EsProfesionalMixin


class Home(EsProfesionalMixin, TemplateView):
    template_name = f"{app_name}/home.html"


home_view = Home.as_view()
