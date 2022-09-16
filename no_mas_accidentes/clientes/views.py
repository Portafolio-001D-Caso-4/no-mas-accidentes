import datetime

from django.views.generic import TemplateView

from no_mas_accidentes.clientes.constants import app_name
from no_mas_accidentes.clientes.mixins import EsClienteMixin
from no_mas_accidentes.clientes.models import FacturaMensual
from no_mas_accidentes.servicios.business_logic.servicios import (
    traer_context_data_de_servicios_por_empresa,
)
from no_mas_accidentes.servicios.models import Evento


class Home(EsClienteMixin, TemplateView):
    template_name = f"{app_name}/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        id_empresa = self.request.user.empresa_id
        factura_mensual: FacturaMensual = FacturaMensual.objects.filter(
            contrato__empresa_id=id_empresa
        ).last()
        context["num_visitas"] = factura_mensual.num_visitas
        context["num_capacitaciones"] = factura_mensual.num_capacitaciones
        context["num_asesorias"] = factura_mensual.num_asesorias
        context["num_llamadas"] = factura_mensual.num_llamadas

        context["max_num_visitas"] = factura_mensual.contrato.max_visitas_mensuales
        context[
            "max_num_capacitaciones"
        ] = factura_mensual.contrato.max_capacitaciones_mensuales
        context["max_num_asesorias"] = factura_mensual.contrato.max_asesorias_mensuales

        context["num_llamadas_extra"] = factura_mensual.num_llamadas_fuera_horario
        num_accidentes = Evento.objects.filter(
            fecha__gte=factura_mensual.expiracion - datetime.timedelta(days=30),
            tipo="ACCIDENTE",
        ).count()
        num_multas = Evento.objects.filter(
            fecha__gte=factura_mensual.expiracion - datetime.timedelta(days=30),
            tipo="MULTA",
        ).count()

        context["num_accidentes"] = num_accidentes
        context["num_multas"] = num_multas

        agendas = traer_context_data_de_servicios_por_empresa(id_empresa=id_empresa)
        context["agendas"] = agendas
        return context


home_view = Home.as_view()
