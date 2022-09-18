import arrow
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect

from no_mas_accidentes.clientes.models import FacturaMensual


class EsClienteYAdeudadoMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.groups.filter(name="cliente").exists()

    def empresa_tiene_deudas(self):
        empresa = self.request.user.empresa
        factura_no_pagada = FacturaMensual.objects.filter(
            contrato__empresa=empresa,
            expiracion__lte=arrow.utcnow().datetime,
            es_pagado=False,
        ).exists()
        if factura_no_pagada:
            return True
        return False

    def handle_vista_factura_no_pagada(self):
        return redirect("clientes:empresa_adeudada")

    def dispatch(self, request, *args, **kwargs):
        user_test_result = self.get_test_func()()
        if not user_test_result:
            return self.handle_no_permission()
        if self.empresa_tiene_deudas():
            return self.handle_vista_factura_no_pagada()
        return super().dispatch(request, *args, **kwargs)


class EsClienteMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.groups.filter(name="cliente").exists()
