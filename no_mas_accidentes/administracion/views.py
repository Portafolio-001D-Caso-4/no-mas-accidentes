from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, TemplateView

from no_mas_accidentes.administracion.constants import app_name
from no_mas_accidentes.administracion.forms import CrearClienteForm
from no_mas_accidentes.administracion.mixins import EsAdministradorMixin
from no_mas_accidentes.users.models import User


class HomeView(EsAdministradorMixin, TemplateView):
    template_name = f"{app_name}/home.html"


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
            queryset = queryset.filter(rut=str(filtro_rut).upper())
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filtro_rut"] = self.request.GET.get("filtro_rut", "")
        return context


class CrearClienteView(EsAdministradorMixin, SuccessMessageMixin, CreateView):
    template_name = f"{app_name}/crear_cliente.html"
    form_class = CrearClienteForm
    success_url = reverse_lazy(f"{app_name}:mantenedor_clientes_lista")

    def get_success_message(self, cleaned_data):
        return (
            f"Cliente {self.object.id} - {self.object.email} creado satisfactoriamente"
        )


home_view = HomeView.as_view()
lista_clientes_view = ListaClientesView.as_view()
crear_cliente_view = CrearClienteView.as_view()
