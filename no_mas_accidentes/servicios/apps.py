from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ServiciosConfig(AppConfig):
    name = "no_mas_accidentes.servicios"
    verbose_name = _("Servicios")

    def ready(self):
        try:
            import no_mas_accidentes.servicios.signals  # noqa F401
        except ImportError:
            pass
