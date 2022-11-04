from collections import Counter

import arrow
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Fieldset, Layout
from django import forms
from django.contrib import messages
from django.core.validators import MaxValueValidator, MinValueValidator
from django.forms import ModelForm, widgets

from no_mas_accidentes.clientes.models import Empresa
from no_mas_accidentes.servicios.models import (
    Checklist,
    OportunidadDeMejora,
    Participante,
    Servicio,
)


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


class ActualizarVisitaForm(ModelForm):
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
        visita = super().save(commit=False)
        if self.terminado:
            visita.realizado_en = arrow.utcnow().datetime
        visita.save()
        return visita


class ActualizarChecklistForm(forms.Form):
    numero_de_items = forms.IntegerField(
        widget=forms.HiddenInput(),
        validators=[MinValueValidator(3), MaxValueValidator(15)],
    )

    def __init__(self, *args, **kwargs):
        numero_de_items = kwargs.pop("numero_de_items", 3)
        print("numero de items", numero_de_items)
        self.id_servicio = kwargs.pop("id_servicio")
        self.request = kwargs.pop("request")
        super().__init__(*args, **kwargs)
        self.fields["numero_de_items"].initial = numero_de_items
        for index in range(int(numero_de_items)):
            self.fields[f"item_{index+1}"] = forms.CharField(
                min_length=10, max_length=256
            )
            self.fields[f"item_{index+1}_respuesta"] = forms.BooleanField(
                required=False
            )

    def clean(self):
        cleaned_data = self.cleaned_data
        preguntas = list(self.cleaned_data.values())
        preguntas = [
            pregunta for pregunta in preguntas if pregunta not in (False, True, None)
        ]
        items_duplicados = [k for k, v in Counter(preguntas).items() if v > 1]

        if items_duplicados:
            cleaned_data_con_items_duplicados = cleaned_data.copy()
            for k, v in cleaned_data_con_items_duplicados.items():
                if v in items_duplicados:
                    self.add_error(field=k, error="Este item está duplicado")
            messages.warning(
                request=self.request,
                message=f"Existen items duplicados en el checklist: {items_duplicados}",
            )
        return cleaned_data

    def save(self, commit: bool = True):
        cleaned_data = self.cleaned_data.copy()
        cleaned_data.pop("numero_de_items")
        items_nuevos = {}
        for key, value in cleaned_data.items():
            if "item" in key and "respuesta" not in key:
                items_nuevos[value] = cleaned_data[f"{key}_respuesta"]
        checklist = Checklist.objects.get(servicio_id=self.id_servicio)
        if checklist.items == items_nuevos:
            messages.info(
                request=self.request,
                message="Los items a actualizar son iguales a los anteriores, no se ha actualizado el checklist.",
            )
            return
        messages.success(request=self.request, message="Se ha actualizado el checklist")
        checklist.items = items_nuevos
        checklist.save()
        return checklist


class ActualizarOportunidadDeMejoraVisitaForm(ModelForm):
    class Meta:
        model = OportunidadDeMejora
        fields = ("contenido",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.terminado = False
        for fieldname in self.fields:
            self.fields[fieldname].required = True


class ActualizarOportunidadDeMejoraVisitaFormSetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form_method = "post"
        self.render_required_fields = True
        self.layout = Layout(
            Fieldset("Actividad de mejora #{{forloop.counter}}"), "contenido"
        )


class ActualizarAsesoriaFiscalizacionForm(ModelForm):
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
        asesoria_fiscalizacion = super().save(commit=False)
        if self.terminado:
            asesoria_fiscalizacion.realizado_en = arrow.utcnow().datetime
        asesoria_fiscalizacion.save()
        return asesoria_fiscalizacion
