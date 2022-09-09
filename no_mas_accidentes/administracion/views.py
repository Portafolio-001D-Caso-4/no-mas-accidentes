from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.messages.views import SuccessMessageMixin
from django.core.files.storage import FileSystemStorage
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, TemplateView, UpdateView
from rest_framework.decorators import api_view

from no_mas_accidentes.administracion.business_logic.contrato import (
    generar_pdf_contrato_base,
)
from no_mas_accidentes.administracion.constants import app_name
from no_mas_accidentes.administracion.forms import (
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
from no_mas_accidentes.clientes.models import Contrato, Empresa
from no_mas_accidentes.profesionales.models import Profesional
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
        context["empresa"] = Empresa.objects.get(pk=self.kwargs["pk"])
        return context


lista_empresas_view = ListaEmpresasView.as_view()
crear_empresa_view = CrearEmpresaView.as_view()
detalle_empresa_informacion_view = DetalleEmpresaInformacionView.as_view()
detalle_empresa_contratos_view = DetalleEmpresaContratosView.as_view()


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
