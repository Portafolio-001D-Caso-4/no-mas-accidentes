from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.messages.views import SuccessMessageMixin
from django.core.files.storage import FileSystemStorage
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    CreateView,
    ListView,
    RedirectView,
    TemplateView,
    UpdateView,
)
from rest_framework.decorators import api_view

from no_mas_accidentes.administracion.business_logic.contrato import (
    generar_pdf_contrato_base,
)
from no_mas_accidentes.administracion.constants import (
    INFORMACION_EMPRESA_PREVENCION_CHILE,
    app_name,
)
from no_mas_accidentes.administracion.forms import (
    ActualizarContratoForm,
    ActualizarDetalleClienteForm,
    ActualizarDetalleEmpresaForm,
    ActualizarDetalleProfesionalForm,
    CrearClienteForm,
    CrearEmpresaForm,
    CrearProfesionalForm,
)
from no_mas_accidentes.administracion.mixins import (
    EsAdministradorMixin,
    PassRequestToFormViewMixin,
    usuario_es_administrador,
)
from no_mas_accidentes.administracion.tasks import enviar_recordatorio_no_pago
from no_mas_accidentes.clientes.models import Contrato, Empresa, FacturaMensual
from no_mas_accidentes.profesionales.models import Profesional
from no_mas_accidentes.servicios.constants import TIPOS_DE_SERVICIOS
from no_mas_accidentes.servicios.models import Servicio
from no_mas_accidentes.users.models import User


class HomeView(EsAdministradorMixin, TemplateView):
    template_name = f"{app_name}/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["num_clientes"] = User.objects.filter(groups__name="cliente").count()
        context["num_empresas"] = Empresa.objects.all().count()
        context["num_profesionales"] = Profesional.objects.all().count()
        return context


home_view = HomeView.as_view()


# -- Mantenedor de Clientes --
class ListaClientesView(EsAdministradorMixin, ListView):
    queryset = User.objects.filter(groups__name="cliente").all()
    fields = "__all__"
    success_url = reverse_lazy(f"{app_name}:mantenedor_clientes_lista")
    ordering = "id"
    paginate_by = 10
    template_name = f"{app_name}/lista_clientes.html"

    def get_queryset(self):
        filtro_rut = self.request.GET.get("filtro_rut")
        queryset = self.queryset.order_by(self.ordering)
        if filtro_rut:
            rut_a_buscar = str(filtro_rut).upper()
            queryset = queryset.filter(
                Q(rut=rut_a_buscar) | Q(empresa__rut=rut_a_buscar)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filtro_rut"] = self.request.GET.get("filtro_rut", "")
        return context


class CrearClienteView(
    EsAdministradorMixin, PassRequestToFormViewMixin, SuccessMessageMixin, CreateView
):
    template_name = f"{app_name}/crear_cliente.html"
    form_class = CrearClienteForm
    success_url = reverse_lazy(f"{app_name}:mantenedor_clientes_lista")

    def get_success_message(self, cleaned_data):
        return (
            f"Cliente {self.object.id} - {self.object.email} creado satisfactoriamente"
        )


class DetalleClienteInformacionView(
    EsAdministradorMixin, SuccessMessageMixin, UpdateView
):
    template_name = f"{app_name}/detalle_cliente/informacion.html"
    form_class = ActualizarDetalleClienteForm
    queryset = User.objects.filter(groups__name="cliente").all()

    def get_success_url(self) -> str:
        return reverse_lazy(
            f"{app_name}:mantenedor_clientes_detalle_informacion",
            kwargs={"pk": self.object.pk},
        )

    def get_success_message(self, cleaned_data):
        return f"Cliente {self.object.id} - {self.object.email} actualizado satisfactoriamente"


lista_clientes_view = ListaClientesView.as_view()
crear_cliente_view = CrearClienteView.as_view()
detalle_cliente_informacion_view = DetalleClienteInformacionView.as_view()


# -- Mantenedor de profesionales --


class ListaProfesionalesView(EsAdministradorMixin, ListView):
    queryset = User.objects.filter(groups__name="profesional").all()
    fields = "__all__"
    success_url = reverse_lazy(f"{app_name}:mantenedor_profesionales_lista")
    ordering = "id"
    paginate_by = 10
    template_name = f"{app_name}/lista_profesionales.html"

    def get_queryset(self):
        filtro_rut = self.request.GET.get("filtro_rut")
        queryset = self.queryset.order_by(self.ordering)
        if filtro_rut:
            rut_a_buscar = str(filtro_rut).upper()
            queryset = queryset.filter(rut=rut_a_buscar)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filtro_rut"] = self.request.GET.get("filtro_rut", "")
        return context


class CrearProfesionalView(
    EsAdministradorMixin, PassRequestToFormViewMixin, SuccessMessageMixin, CreateView
):
    template_name = f"{app_name}/crear_profesional.html"
    form_class = CrearProfesionalForm
    success_url = reverse_lazy(f"{app_name}:mantenedor_profesionales_lista")

    def get_success_message(self, cleaned_data):
        return f"Profesional {self.object.id} - {self.object.email} creado satisfactoriamente"


class DetalleProfesionalInformacionView(
    EsAdministradorMixin, SuccessMessageMixin, UpdateView
):
    template_name = f"{app_name}/detalle_profesional/informacion.html"
    form_class = ActualizarDetalleProfesionalForm
    queryset = User.objects.filter(groups__name="profesional").all()

    def get_success_url(self) -> str:
        return reverse_lazy(
            f"{app_name}:mantenedor_profesionales_detalle_informacion",
            kwargs={"pk": self.object.pk},
        )

    def get_success_message(self, cleaned_data):
        return f"Profesional {self.object.id} - {self.object.email} actualizado satisfactoriamente"


lista_profesionales_view = ListaProfesionalesView.as_view()
crear_profesional_view = CrearProfesionalView.as_view()
detalle_profesional_informacion_view = DetalleProfesionalInformacionView.as_view()


# -- Mantenedor de empresas --


class ListaEmpresasView(EsAdministradorMixin, ListView):
    queryset = Empresa.objects.all()
    fields = "__all__"
    success_url = reverse_lazy(f"{app_name}:mantenedor_empresas_lista")
    ordering = "id"
    paginate_by = 10
    template_name = f"{app_name}/lista_empresas.html"

    def get_queryset(self):
        filtro_rut = self.request.GET.get("filtro_rut")
        queryset = self.queryset.order_by(self.ordering)
        if filtro_rut:
            rut_a_buscar = str(filtro_rut).upper()
            queryset = queryset.filter(rut=rut_a_buscar)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filtro_rut"] = self.request.GET.get("filtro_rut", "")
        return context


class CrearEmpresaView(
    EsAdministradorMixin, PassRequestToFormViewMixin, SuccessMessageMixin, CreateView
):
    template_name = f"{app_name}/crear_empresa.html"
    form_class = CrearEmpresaForm
    success_url = reverse_lazy(f"{app_name}:mantenedor_empresas_lista")

    def get_success_message(self, cleaned_data):
        return (
            f"Empresa {self.object.id} - {self.object.nombre} creada satisfactoriamente"
        )


class DetalleEmpresaInformacionView(
    EsAdministradorMixin, SuccessMessageMixin, UpdateView
):
    template_name = f"{app_name}/detalle_empresa/informacion.html"
    form_class = ActualizarDetalleEmpresaForm
    queryset = Empresa.objects.all()

    def get_success_url(self) -> str:
        return reverse_lazy(
            f"{app_name}:mantenedor_empresas_detalle_informacion",
            kwargs={"pk": self.object.pk},
        )

    def get_success_message(self, cleaned_data):
        return f"Empresa {self.object.id} - {self.object.nombre} actualizada satisfactoriamente"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["empresa"] = self.object
        return context


class DetalleEmpresaContratosView(EsAdministradorMixin, ListView):
    queryset = Contrato.objects.all()
    fields = "__all__"
    success_url = reverse_lazy(f"{app_name}:mantenedor_empresas_detalle_contratos")
    ordering = "id"
    paginate_by = 10
    template_name = f"{app_name}/detalle_empresa/contratos.html"

    def get_queryset(self):
        queryset = self.queryset.order_by(self.ordering)
        # filtrar por PK de empresa
        queryset = queryset.filter(empresa_id=self.kwargs["pk"])
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        empresa = Empresa.objects.get(pk=self.kwargs["pk"])
        context["empresa"] = empresa
        return context


class DetalleEmpresaContratoView(EsAdministradorMixin, SuccessMessageMixin, UpdateView):
    template_name = f"{app_name}/detalle_empresa/detalle_contrato.html"
    form_class = ActualizarContratoForm
    queryset = Contrato.objects.all()

    def get_success_url(self) -> str:
        return reverse_lazy(
            f"{app_name}:mantenedor_empresas_detalle_contratos",
            kwargs={"pk": self.kwargs["pk"]},
        )

    def get_success_message(self, cleaned_data):
        return "Contrato cargado satisfactoriamente"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["empresa"] = self.object
        return context

    def get_object(self):
        return self.queryset.get(
            id=self.kwargs["contrato_id"], empresa_id=self.kwargs["pk"]
        )


class DetalleEmpresaPagosView(EsAdministradorMixin, ListView):
    queryset = FacturaMensual.objects.all()
    fields = "__all__"
    success_url = reverse_lazy(f"{app_name}:mantenedor_empresas_detalle_pagos")
    ordering = "-expiracion"
    paginate_by = 10
    template_name = f"{app_name}/detalle_empresa/pagos.html"

    def get_queryset(self):
        queryset = self.queryset.order_by(self.ordering)
        queryset = queryset.filter(contrato__empresa_id=self.kwargs["pk"])
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        empresa = Empresa.objects.get(pk=self.kwargs["pk"])
        context["empresa"] = empresa
        return context


class DetalleEmpresaPagoView(EsAdministradorMixin, SuccessMessageMixin, TemplateView):
    template_name = f"{app_name}/detalle_empresa/detalle_pago.html"
    queryset = FacturaMensual.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["factura_mensual"] = self.get_object()
        context["empresa"] = context["factura_mensual"].contrato.empresa
        context["informacion_empresa"] = INFORMACION_EMPRESA_PREVENCION_CHILE
        return context

    def get_object(self):
        return self.queryset.get(
            id=self.kwargs["factura_mensual_id"], contrato__empresa_id=self.kwargs["pk"]
        )


lista_empresas_view = ListaEmpresasView.as_view()
crear_empresa_view = CrearEmpresaView.as_view()
detalle_empresa_informacion_view = DetalleEmpresaInformacionView.as_view()
detalle_empresa_contratos_view = DetalleEmpresaContratosView.as_view()
detalle_empresa_contrato_view = DetalleEmpresaContratoView.as_view()
detalle_empresa_pagos_view = DetalleEmpresaPagosView.as_view()
detalle_empresa_pago_view = DetalleEmpresaPagoView.as_view()


class ListaServiciosView(EsAdministradorMixin, ListView):
    queryset = Servicio.objects.all()
    fields = "__all__"
    success_url = reverse_lazy(f"{app_name}:servicios_lista")
    ordering = "-agendado_para"
    paginate_by = 10
    template_name = f"{app_name}/lista_servicios.html"

    def get_queryset(self):
        filtro_rut = self.request.GET.get("filtro_rut")
        filtro_empresa_seleccionada = self.request.GET.get(
            "filtro_empresa_seleccionada"
        )
        filtro_tipo_seleccionado = self.request.GET.get("filtro_tipo_seleccionado")
        filtro_es_realizado = self.request.GET.get("filtro_es_realizado")
        queryset = self.queryset.order_by(self.ordering)
        if filtro_rut:
            rut_a_buscar = str(filtro_rut).upper()
            queryset = queryset.filter(rut=rut_a_buscar)
        if filtro_empresa_seleccionada:
            queryset = queryset.filter(empresa_id=int(filtro_empresa_seleccionada))
        if filtro_tipo_seleccionado:
            queryset = queryset.filter(tipo=filtro_tipo_seleccionado)
        if filtro_es_realizado == "PENDIENTE":
            queryset = queryset.filter(realizado_en__isnull=True)
        elif filtro_es_realizado == "REALIZADA":
            queryset = queryset.filter(realizado_en__isnull=False)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filtro_rut"] = self.request.GET.get("filtro_rut", "")
        context["filtro_tipo_seleccionado"] = self.request.GET.get(
            "filtro_tipo_seleccionado", ""
        )
        context["filtro_es_realizado"] = self.request.GET.get("filtro_es_realizado", "")
        # solo puede ver sus empresas asignadas
        context["filtro_tipos"] = TIPOS_DE_SERVICIOS
        context["filtro_empresas"] = Empresa.objects.all()
        filtro_empresa_seleccionada = self.request.GET.get(
            "filtro_empresa_seleccionada", ""
        )
        context["filtro_empresa_seleccionada"] = (
            int(filtro_empresa_seleccionada) if filtro_empresa_seleccionada else ""
        )
        return context


lista_servicios_view = ListaServiciosView.as_view()


@login_required
@user_passes_test(test_func=usuario_es_administrador)
@api_view(["GET"])
def descarga_contrato_base_view(request, pk):
    contrato = get_object_or_404(Contrato, pk=pk)
    nombre_archivo = generar_pdf_contrato_base(contrato=contrato)
    directorio = FileSystemStorage("/tmp")
    with directorio.open(f"{nombre_archivo}.pdf") as pdf:
        response = HttpResponse(pdf, content_type="application/pdf")
        response["Content-Disposition"] = f'attachment; filename="{nombre_archivo}.pdf"'
        return response


class EnviarRecordatorioNoPagoView(EsAdministradorMixin, RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        self.url = reverse(
            "administracion:mantenedor_empresas_detalle_pagos",
            kwargs={"pk": self.kwargs["pk"]},
        )
        url_de_pago = self.request.build_absolute_uri(reverse("clientes:realizar_pago"))
        enviar_recordatorio_no_pago.delay(
            id_factura_mensual=int(self.kwargs["factura_mensual_id"]),
            url_de_pago=url_de_pago,
        )
        messages.success(self.request, "Email de recordatorio de pago enviado")
        return super().get_redirect_url(*args, **kwargs)


enviar_recordatorio_no_pago_view = EnviarRecordatorioNoPagoView.as_view()
