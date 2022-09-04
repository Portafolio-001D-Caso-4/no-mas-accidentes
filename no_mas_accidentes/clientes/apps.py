from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ClientesConfig(AppConfig):
    name = "no_mas_accidentes.clientes"
    verbose_name = _("Clientes")

    def ready(self):
        try:
            import no_mas_accidentes.clientes.signals  # noqa F401
        except ImportError:
            pass
