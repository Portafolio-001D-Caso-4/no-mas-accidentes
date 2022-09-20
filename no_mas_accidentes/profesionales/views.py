import arrow
from django.db.models import Count
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, TemplateView

from no_mas_accidentes.clientes.models import Empresa
from no_mas_accidentes.profesionales.constants import app_name
from no_mas_accidentes.profesionales.forms import DetalleEmpresaForm
from no_mas_accidentes.profesionales.mixins import EsProfesionalMixin
from no_mas_accidentes.servicios.business_logic import (
    servicios as business_logic_servicios,
)
from no_mas_accidentes.servicios.constants import TIPOS_DE_SERVICIOS, TiposDeServicio
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


class ListaEmpresasAsignadasView(EsProfesionalMixin, ListView):
    queryset = Empresa.objects.all()
    fields = "__all__"
    success_url = reverse_lazy(f"{app_name}:empresas_asignadas_lista")
    ordering = "id"
    paginate_by = 10
    template_name = f"{app_name}/lista_empresas_asignadas.html"

    def get_queryset(self):
        filtro_rut = self.request.GET.get("filtro_rut")
        queryset = self.queryset.order_by(self.ordering)
        # solo puede ver sus empresas asignadas
        queryset = queryset.filter(profesional_asignado_id=self.request.user.pk)
        if filtro_rut:
            rut_a_buscar = str(filtro_rut).upper()
            queryset = queryset.filter(rut=rut_a_buscar)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filtro_rut"] = self.request.GET.get("filtro_rut", "")
        return context


class DetalleEmpresaInformacionView(EsProfesionalMixin, DetailView):
    template_name = f"{app_name}/detalle_empresa/informacion.html"
    queryset = Empresa.objects.all()

    def get_queryset(self):
        return self.queryset.filter(profesional_asignado_id=self.request.user.pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["empresa"] = self.object
        context["form"] = DetalleEmpresaForm(instance=self.object)
        return context


home_view = Home.as_view()
lista_empresas_asignadas_view = ListaEmpresasAsignadasView.as_view()
detalle_empresa_informacion_view = DetalleEmpresaInformacionView.as_view()


class Empresas:
    pass


class ListaServiciosAsignadosView(EsProfesionalMixin, ListView):
    queryset = Servicio.objects.all()
    fields = "__all__"
    success_url = reverse_lazy(f"{app_name}:servicios_asignados_lista")
    ordering = "-agendado_para"
    paginate_by = 10
    template_name = f"{app_name}/lista_servicios_asignados.html"

    def get_queryset(self):
        filtro_rut = self.request.GET.get("filtro_rut")
        filtro_empresa_seleccionada = self.request.GET.get(
            "filtro_empresa_seleccionada"
        )
        filtro_tipo_seleccionado = self.request.GET.get("filtro_tipo_seleccionado")
        filtro_es_realizado = self.request.GET.get("filtro_es_realizado")
        queryset = self.queryset.order_by(self.ordering)
        # solo puede ver sus servicios asignadas
        queryset = queryset.filter(profesional_id=self.request.user.pk)
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
        context["filtro_empresas"] = Empresa.objects.filter(
            profesional_asignado_id=self.request.user.pk
        )
        filtro_empresa_seleccionada = self.request.GET.get(
            "filtro_empresa_seleccionada", ""
        )
        context["filtro_empresa_seleccionada"] = (
            int(filtro_empresa_seleccionada) if filtro_empresa_seleccionada else ""
        )
        return context


lista_servicios_asignados_view = ListaServiciosAsignadosView.as_view()
