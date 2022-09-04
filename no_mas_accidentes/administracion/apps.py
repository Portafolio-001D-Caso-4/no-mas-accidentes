from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AdministracionConfig(AppConfig):
    name = "no_mas_accidentes.administracion"
    verbose_name = _("Administracion")

    def ready(self):
        try:
            import no_mas_accidentes.administracion.signals  # noqa F401
        except ImportError:
            pass
