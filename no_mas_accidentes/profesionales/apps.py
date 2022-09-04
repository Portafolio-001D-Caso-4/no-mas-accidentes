from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ProfesionalesConfig(AppConfig):
    name = "no_mas_accidentes.profesionales"
    verbose_name = _("Profesionales")

    def ready(self):
        try:
            import no_mas_accidentes.profesionales.signals  # noqa F401
        except ImportError:
            pass
