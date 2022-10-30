import arrow
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Fieldset, Layout
from django.forms import ModelForm, widgets

from no_mas_accidentes.clientes.models import Empresa
from no_mas_accidentes.servicios.models import Participante, Servicio


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


class ActualizarCapacitacionForm(ModelForm):
    class Meta:
        model = Servicio
        readonly_fields = (
            "profesional",
            "empresa",
            "agendado_para",
        )
        fields = readonly_fields + ("motivo", "contenido", "materiales")

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
        capacitacion = super().save(commit=False)
        if self.terminado:
            capacitacion.realizado_en = arrow.utcnow().datetime
        capacitacion.save()
        return capacitacion


class ActualizarAsistenciaParticipanteCapacitacionForm(ModelForm):
    class Meta:
        model = Participante
        readonly_fields = ("rut", "nombre", "email")
        fields = readonly_fields + ("asiste",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.terminado = False
        for fieldname in self.Meta.readonly_fields:
            self.fields[fieldname].disabled = True


class ActualizarAsistenciaParticipantesFormSetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form_method = "post"
        self.render_required_fields = True
        self.layout = Layout(
            Fieldset("Participante #{{forloop.counter}}"),
            "rut",
            "nombre",
            "email",
            "asiste",
        )
