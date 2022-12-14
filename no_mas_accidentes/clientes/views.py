import arrow
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.forms import modelformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, RedirectView, TemplateView
from transbank.error.transaction_commit_error import TransactionCommitError
from transbank.webpay.webpay_plus.transaction import Transaction

from no_mas_accidentes.administracion.constants import (
    INFORMACION_EMPRESA_PREVENCION_CHILE,
)
from no_mas_accidentes.administracion.mixins import PassRequestToFormViewMixin
from no_mas_accidentes.clientes.business_logic.pagos import realizar_pago_ultima_factura
from no_mas_accidentes.clientes.constants import app_name
from no_mas_accidentes.clientes.forms import (
    ActualizarMultaAsesoriaForm,
    ActualizarParticipanteCapacitacionForm,
    ActualizarParticipantesFormSetHelper,
    SolicitarAsesoriaDeEmergenciaForm,
    SolicitarAsesoriaForm,
    SolicitarCapacitacionForm,
    SolicitarVisitaForm,
)
from no_mas_accidentes.clientes.mixins import EsClienteMixin, EsClienteYAdeudadoMixin
from no_mas_accidentes.clientes.models import Empresa, FacturaMensual
from no_mas_accidentes.servicios.business_logic.reportes import (
    traer_informacion_reporte_cliente,
)
from no_mas_accidentes.servicios.business_logic.servicios import (
    traer_context_data_de_servicios_por_empresa,
)
from no_mas_accidentes.servicios.constants import TiposDeServicio
from no_mas_accidentes.servicios.models import Evento, Participante, Servicio


class Home(EsClienteYAdeudadoMixin, TemplateView):
    template_name = f"{app_name}/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        id_empresa = self.request.user.empresa_id
        factura_mensual: FacturaMensual = (
            FacturaMensual.objects.filter(contrato__empresa_id=id_empresa)
            .order_by("expiracion")
            .last()
        )
        print(factura_mensual)
        context["num_visitas"] = (
            factura_mensual.num_visitas + factura_mensual.num_visitas_extra
        )
        context["num_capacitaciones"] = (
            factura_mensual.num_capacitaciones
            + factura_mensual.num_capacitaciones_extra
        )
        context["num_asesorias"] = (
            factura_mensual.num_asesorias + factura_mensual.num_asesorias_extra
        )
        context["num_llamadas"] = factura_mensual.num_llamadas

        context["max_num_visitas"] = factura_mensual.contrato.max_visitas_mensuales
        context[
            "max_num_capacitaciones"
        ] = factura_mensual.contrato.max_capacitaciones_mensuales
        context["max_num_asesorias"] = factura_mensual.contrato.max_asesorias_mensuales

        context["num_llamadas_extra"] = factura_mensual.num_llamadas_fuera_horario
        num_accidentes = Evento.objects.filter(
            fecha__gte=arrow.get(factura_mensual.expiracion).replace(day=1).datetime,
            fecha__lte=factura_mensual.expiracion,
            tipo="ACCIDENTE",
        ).count()
        num_multas = Evento.objects.filter(
            fecha__gte=arrow.get(factura_mensual.expiracion).replace(day=1).datetime,
            fecha__lte=factura_mensual.expiracion,
            tipo="MULTA",
        ).count()

        context["num_accidentes"] = num_accidentes
        context["num_multas"] = num_multas

        agendas = traer_context_data_de_servicios_por_empresa(id_empresa=id_empresa)
        context["agendas"] = agendas
        return context


class EmpresaAdeudadaView(EsClienteMixin, TemplateView):
    template_name = f"{app_name}/empresa-adeudada.html"


@method_decorator(csrf_exempt, name="dispatch")
class RealizarPagoView(EsClienteMixin, TemplateView):
    template_name = f"{app_name}/pagos/realizar-pago.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["informacion_empresa"] = INFORMACION_EMPRESA_PREVENCION_CHILE
        context["empresa"] = self.request.user.empresa
        factura_mensual: FacturaMensual = (
            FacturaMensual.objects.filter(
                contrato__empresa=context["empresa"], es_pagado=False
            )
            .order_by("expiracion")
            .last()
        )
        context["factura_mensual"] = factura_mensual
        context["pago_realizado"] = False

        amount = factura_mensual.total
        buy_order = f"e{arrow.utcnow().int_timestamp}"
        session_id = str(self.request.user.id)
        return_url = self.request.build_absolute_uri(
            location=reverse("clientes:recepcion_transaccion")
        )
        response = Transaction.create(buy_order, session_id, amount, return_url)
        context["transbank_url"] = response.url
        context["transbank_token"] = response.token

        return context


@method_decorator(csrf_exempt, name="dispatch")
class RecepcionTransaccionView(RedirectView):
    permanent = False
    query_string = True

    def get_redirect_url(self, *args, **kwargs):
        request = self.request
        token = request.GET.get("token_ws") or request.POST.get("token_ws")
        try:
            response = Transaction.commit(token=token)
            response_status_code = response.response_code
            response_status = response.status
            id_usuario = response.session_id
        except TransactionCommitError as error:
            response_status = error.message
            response_status_code = error.code
            id_usuario = None
        if response_status_code != 0 or response_status != "AUTHORIZED":
            messages.warning(
                self.request,
                f"El pago ha sido rechazado, intente nuevamente en unos minutos o cont??ctese "
                f"con su proveedor de medio de pago. C??digo de error: {response_status_code} "
                f"Estado transacci??n: {response_status}",
            )
            self.url = reverse("clientes:realizar_pago")
        else:
            realizar_pago_ultima_factura(id_cliente=int(id_usuario))
            messages.success(
                self.request,
                "Pago realizado satisfactoriamente, puede seguir utilizando el servicio.",
            )
            self.url = reverse("clientes:transaccion_exitosa")
        return super().get_redirect_url(*args, **kwargs)


class TransaccionExitosaView(EsClienteMixin, TemplateView):
    template_name = f"{app_name}/pagos/realizar-pago.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["informacion_empresa"] = INFORMACION_EMPRESA_PREVENCION_CHILE
        context["empresa"] = self.request.user.empresa
        factura_mensual: FacturaMensual = (
            FacturaMensual.objects.filter(contrato__empresa=context["empresa"])
            .order_by("expiracion")
            .last()
        )
        context["factura_mensual"] = factura_mensual
        context["pago_realizado"] = True

        return context


home_view = Home.as_view()
empresa_adeudada_view = EmpresaAdeudadaView.as_view()
realizar_pago_view = RealizarPagoView.as_view()
recepcion_transaccion_view = RecepcionTransaccionView.as_view()
transaccion_exitosa_view = TransaccionExitosaView.as_view()


class ReporteClienteView(EsClienteMixin, TemplateView):
    template_name = f"{app_name}/reporte.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["informacion_empresa"] = INFORMACION_EMPRESA_PREVENCION_CHILE
        context["empresa"] = self.request.user.empresa

        (
            context["servicios"],
            context["fecha_hasta"],
        ) = traer_informacion_reporte_cliente(empresa_id=self.request.user.empresa.id)
        facturas_mensuales: FacturaMensual = (
            FacturaMensual.objects.filter(contrato__empresa=context["empresa"])
            .order_by("expiracion")
            .all()
        )
        context["facturas_mensuales"] = facturas_mensuales
        return context


reporte_cliente_view = ReporteClienteView.as_view()


class SolicitarAsesoriaDeEmergencia(
    EsClienteMixin, PassRequestToFormViewMixin, SuccessMessageMixin, CreateView
):
    template_name = f"{app_name}/solicitar_asesoria_emergencia.html"
    form_class = SolicitarAsesoriaDeEmergenciaForm
    success_url = reverse_lazy(f"{app_name}:home")

    def get_success_message(self, cleaned_data):
        servicio = self.object.servicio
        return (
            f"Asesor??a de emergencia {self.object.id} "
            f"creada satisfactoriamente: Profesional {servicio.profesional} "
            f"- Horario {arrow.get(servicio.agendado_para).to('America/Santiago').format('YYYY-MM-DD HH:mm:ss')}"
        )


solicitar_asesoria_emergencia_view = SolicitarAsesoriaDeEmergencia.as_view()


class SolicitarCapacitacion(
    EsClienteMixin, PassRequestToFormViewMixin, SuccessMessageMixin, CreateView
):
    template_name = f"{app_name}/solicitar_capacitacion.html"
    form_class = SolicitarCapacitacionForm

    def get_success_message(self, cleaned_data):
        return (
            f"Capacitaci??n {self.object.id} "
            f"creada satisfactoriamente: Profesional {self.object.profesional} "
            f"- Horario {arrow.get(self.object.agendado_para).to('America/Santiago').format('YYYY-MM-DD HH:mm:ss')}"
        )

    def get_success_url(self) -> str:
        return reverse_lazy(
            f"{app_name}:modificar_participantes_capacitacion",
            kwargs={"pk": self.object.pk},
        )


def modificar_participantes_capacitacion_view(request, pk: int):
    capacitacion: Servicio = Servicio.objects.filter(
        tipo=TiposDeServicio.CAPACITACION, empresa_id=request.user.empresa_id
    ).get(pk=pk)
    participantes = capacitacion.participante_set.all().order_by("rut")
    helper = ActualizarParticipantesFormSetHelper()
    actualizar_participantes_forms = modelformset_factory(
        Participante,
        form=ActualizarParticipanteCapacitacionForm,
        min_num=capacitacion.num_participantes,
        validate_min=True,
        extra=0,
    )

    if request.method == "POST":
        formset = actualizar_participantes_forms(
            data=request.POST, queryset=participantes
        )
        if formset.is_valid():
            instances = formset.save(commit=False)
            for participante in instances:
                participante.servicio = capacitacion
                participante.save()
            formset.save_m2m()
            messages.success(
                request=request, message="Participantes modificados satisfactoriamente"
            )
            return HttpResponseRedirect(reverse_lazy(f"{app_name}:home"))
    else:
        formset = actualizar_participantes_forms(queryset=participantes)

    return render(
        request,
        f"{app_name}/capacitacion/actualizar_participantes.html",
        {
            "formset": formset,
            "empresa": Empresa.objects.get(pk=capacitacion.empresa_id),
            "helper": helper,
        },
    )


solicitar_capacitacion_view = SolicitarCapacitacion.as_view()
modificar_participantes_capacitacion_view = modificar_participantes_capacitacion_view


class SolicitarVisitaView(
    EsClienteMixin, PassRequestToFormViewMixin, SuccessMessageMixin, CreateView
):
    template_name = f"{app_name}/solicitar_visita.html"
    form_class = SolicitarVisitaForm
    success_url = reverse_lazy(f"{app_name}:home")

    def get_success_message(self, cleaned_data):
        return (
            f"Visita {self.object.id} "
            f"creada satisfactoriamente: Profesional {self.object.profesional} "
            f"- Horario {arrow.get(self.object.agendado_para).to('America/Santiago').format('YYYY-MM-DD HH:mm:ss')}"
        )


solicitar_visita_view = SolicitarVisitaView.as_view()


class SolicitarAsesoria(
    EsClienteMixin, PassRequestToFormViewMixin, SuccessMessageMixin, CreateView
):
    template_name = f"{app_name}/solicitar_asesoria.html"
    form_class = SolicitarAsesoriaForm

    def get_success_message(self, cleaned_data):
        return (
            f"Asesor??a {self.object.id} "
            f"creada satisfactoriamente: Profesional {self.object.profesional} "
            f"- Horario {arrow.get(self.object.agendado_para).to('America/Santiago').format('YYYY-MM-DD HH:mm:ss')}"
        )

    def get_success_url(self) -> str:
        return reverse_lazy(
            f"{app_name}:asesoria_modificar_multa",
            kwargs={"pk": self.object.pk},
        )


def modificar_multa_asesoria_view(request, pk: int):
    asesoria: Servicio = Servicio.objects.filter(
        tipo=TiposDeServicio.ASESORIA_FISCALIZACION
    ).get(pk=pk)
    multa = asesoria.evento_set.filter(tipo="MULTA").first()
    if request.method == "POST":
        if multa:
            # update
            form = ActualizarMultaAsesoriaForm(
                request.POST, request=request, id_servicio=pk, instance=multa
            )
        else:
            # crear
            form = ActualizarMultaAsesoriaForm(
                request.POST, request=request, id_servicio=pk, instance=None
            )
        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Se ha actualizado la multa correctamente",
            )
    else:
        form = ActualizarMultaAsesoriaForm(
            request.POST, request=request, id_servicio=pk, instance=multa
        )
    return render(
        request,
        f"{app_name}/asesoria/actualizar_multa.html",
        {"form": form, "empresa": asesoria.empresa, "object": pk},
    )


solicitar_asesoria_view = SolicitarAsesoria.as_view()
modificar_multa_view = modificar_multa_asesoria_view
