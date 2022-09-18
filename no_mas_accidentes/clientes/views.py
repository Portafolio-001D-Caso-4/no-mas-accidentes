import datetime

import arrow
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from transbank.webpay.webpay_plus.transaction import Transaction

from no_mas_accidentes.administracion.constants import (
    INFORMACION_EMPRESA_PREVENCION_CHILE,
)
from no_mas_accidentes.clientes.constants import app_name
from no_mas_accidentes.clientes.mixins import EsClienteMixin, EsClienteYAdeudadoMixin
from no_mas_accidentes.clientes.models import FacturaMensual
from no_mas_accidentes.servicios.business_logic.servicios import (
    traer_context_data_de_servicios_por_empresa,
)
from no_mas_accidentes.servicios.models import Evento


class Home(EsClienteYAdeudadoMixin, TemplateView):
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


class EmpresaAdeudadaView(EsClienteMixin, TemplateView):
    template_name = f"{app_name}/empresa-adeudada.html"


class RealizarPagoView(EsClienteMixin, TemplateView):
    template_name = f"{app_name}/pagos/realizar-pago.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        amount = 100000
        buy_order = str(arrow.utcnow().int_timestamp)
        session_id = str(self.request.user.id)
        return_url = self.request.build_absolute_uri(
            location=reverse("clientes:transaccion_exitosa")
        )
        response = Transaction.create(buy_order, session_id, amount, return_url)
        context["transbank_url"] = response.url
        context["transbank_token"] = response.token

        context["informacion_empresa"] = INFORMACION_EMPRESA_PREVENCION_CHILE
        context["empresa"] = self.request.user.empresa
        factura_mensual: FacturaMensual = FacturaMensual.objects.filter(
            contrato__empresa=context["empresa"]
        ).last()
        context["factura_mensual"] = factura_mensual
        return context


@method_decorator(csrf_exempt, name="dispatch")
class TransaccionExitosaView(EsClienteMixin, TemplateView):
    template_name = f"{app_name}/pagos/transaccion-exitosa.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #
        # amount = 100000
        # buy_order = str(arrow.utcnow().int_timestamp)
        # session_id = str(self.request.user.id)
        # return_url = self.request.build_absolute_uri(location=reverse("clientes:transaccion_exitosa"))
        # response = Transaction.create(buy_order, session_id, amount, return_url)
        # context['transbank_url'] = response.url
        # context['transbank_token'] = response.token

        return context

    def post(self, request, *args, **kwargs):
        token = request.POST.get("token_ws")
        response = Transaction.commit(token=token)
        context = {
            "buy_order": response.buy_order,
            "session_id": response.session_id,
            "amount": response.amount,
            "response": response,
            "token_ws": token,
            "status": response.status,
            "fecha_transaccion": response.transaction_date,
        }
        # revisar response.status_code para redirigir a otra template
        # response.response_code == 0
        # response.status == "AUTHORIZED"
        return self.render_to_response(context)


home_view = Home.as_view()
empresa_adeudada_view = EmpresaAdeudadaView.as_view()
realizar_pago_view = RealizarPagoView.as_view()
transaccion_exitosa_view = TransaccionExitosaView.as_view()
