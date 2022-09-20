import arrow
from django.db.models import Count
from django.views.generic import TemplateView

from no_mas_accidentes.clientes.models import Empresa
from no_mas_accidentes.profesionales.constants import app_name
from no_mas_accidentes.profesionales.mixins import EsProfesionalMixin
from no_mas_accidentes.servicios.business_logic import (
    servicios as business_logic_servicios,
)
from no_mas_accidentes.servicios.constants import TiposDeServicio
from no_mas_accidentes.servicios.models import Servicio


class Home(EsProfesionalMixin, TemplateView):
    template_name = f"{app_name}/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        mes_actual = arrow.utcnow().datetime.month
        num_servicios_por_tipo = (
            Servicio.objects.filter(
                profesional__usuario=self.request.user, realizado_en__month=mes_actual
            )
            .values("tipo")
            .order_by("tipo")
            .annotate(num_servicios=Count("tipo"))
        )
        num_servicios_por_tipo = {
            servicio_por_tipo["tipo"]: servicio_por_tipo["num_servicios"]
            for servicio_por_tipo in num_servicios_por_tipo
        }
        context["num_visitas"] = num_servicios_por_tipo.get(TiposDeServicio.VISITA, 0)
        context["num_capacitaciones"] = num_servicios_por_tipo.get(
            TiposDeServicio.CAPACITACION, 0
        )
        context["num_asesorias"] = num_servicios_por_tipo.get(
            TiposDeServicio.ASESORIA_EMERGENCIA, 0
        ) + num_servicios_por_tipo.get(TiposDeServicio.ASESORIA_FISCALIZACION, 0)
        context["num_llamadas"] = num_servicios_por_tipo.get(TiposDeServicio.LLAMADA, 0)
        context["num_accidentes"] = num_servicios_por_tipo.get(
            TiposDeServicio.ASESORIA_EMERGENCIA, 0
        )
        context["porcentaje_accidentabilidad"] = 20  # TODO: Calcular esto
        context[
            "agendas"
        ] = business_logic_servicios.traer_context_data_de_servicios_por_profesional(
            id_profesional=self.request.user.pk
        )
        context["num_empresas_asignadas"] = Empresa.objects.filter(
            profesional_asignado_id=self.request.user.pk
        ).count()
        return context


home_view = Home.as_view()
