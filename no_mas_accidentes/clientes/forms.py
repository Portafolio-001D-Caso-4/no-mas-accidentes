from django.db import transaction
from django.forms import DateTimeInput, ModelForm

from no_mas_accidentes.servicios.business_logic.servicios import (
    crear_asesoria_de_emergencia_para_empresa,
)
from no_mas_accidentes.servicios.models import Evento


class SolicitarAsesoriaDeEmergenciaForm(ModelForm):
    class Meta:
        model = Evento
        fields = (
            "fecha",
            "contenido",
        )
        widgets = {
            "fecha": DateTimeInput(attrs={"type": "datetime-local"}),
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super().__init__(*args, **kwargs)

    def save(self, commit: bool = True):
        self.instance.tipo = "ACCIDENTE"
        evento = super().save(commit=False)
        with transaction.atomic():
            if commit:
                evento.save()
            crear_asesoria_de_emergencia_para_empresa(
                id_empresa=self.request.user.empresa_id,
                solicitante=self.request.user,
                accidente=evento,
            )
        return evento
