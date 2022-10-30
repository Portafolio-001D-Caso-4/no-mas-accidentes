import arrow
from django.forms import ModelForm, widgets

from no_mas_accidentes.clientes.models import Empresa
from no_mas_accidentes.servicios.models import Servicio


class DetalleEmpresaForm(ModelForm):
    class Meta:
        model = Empresa
        fields = (
            "nombre",
            "rut",
            "giro",
            "direccion",
            "telefono",
            "profesional_asignado",
            "esta_activa",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["direccion"].widget = widgets.TextInput()
        for fieldname in self.fields:
            self.fields[fieldname].disabled = True


class ActualizarAsesoriaEmergenciaForm(ModelForm):
    class Meta:
        model = Servicio
        readonly_fields = (
            "profesional",
            "empresa",
            "agendado_para",
        )
        fields = readonly_fields + (
            "motivo",
            "contenido",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.terminado = False
        for fieldname in self.Meta.readonly_fields:
            self.fields[fieldname].disabled = True

    def clean(self):
        self.data = self.data.copy()
        if "Finalizar" in self.data:
            self.terminado = True
        else:
            self.terminado = False
        cleaned_data = super().clean()
        return cleaned_data

    def save(self, commit: bool = True):
        asesoria_emergencia = super().save(commit=False)
        if self.terminado:
            asesoria_emergencia.realizado_en = arrow.utcnow().datetime
        asesoria_emergencia.save()
        return asesoria_emergencia
