from django.views.generic import TemplateView

from no_mas_accidentes.clientes.constants import app_name
from no_mas_accidentes.clientes.mixins import EsClienteMixin


class Home(EsClienteMixin, TemplateView):
    template_name = f"{app_name}/home.html"


home_view = Home.as_view()
