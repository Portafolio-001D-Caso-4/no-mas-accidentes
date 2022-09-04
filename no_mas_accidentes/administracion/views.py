from django.views.generic import TemplateView

from no_mas_accidentes.administracion.constants import app_name
from no_mas_accidentes.administracion.mixins import EsAdministradorMixin


class Home(EsAdministradorMixin, TemplateView):
    template_name = f"{app_name}/home.html"


home_view = Home.as_view()
