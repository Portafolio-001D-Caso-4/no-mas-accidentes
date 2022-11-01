import datetime

import arrow
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Fieldset, Layout
from django.core.exceptions import ValidationError
from django.db import transaction
from django.forms import DateTimeInput, ModelForm

from no_mas_accidentes.clientes.models import Empresa, FacturaMensual
from no_mas_accidentes.servicios.business_logic.horarios import (
    traer_horarios_disponibles_de_profesional,
)
from no_mas_accidentes.servicios.business_logic.servicios import (
    crear_asesoria_de_emergencia_para_empresa,
)
from no_mas_accidentes.servicios.constants import (
    TiposDeServicio,
    duracion_en_hrs_por_servicio,
)
from no_mas_accidentes.servicios.models import (
    Checklist,
    ChecklistBase,
    Evento,
    Participante,
    Servicio,
)


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


class SolicitarCapacitacionForm(ModelForm):
    class Meta:
        model = Servicio
        fields = (
            "motivo",
            "num_participantes",
        )

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super().__init__(*args, **kwargs)
        for fieldname in self.fields:
            self.fields[fieldname].required = True

    def save(self, commit: bool = True):
        with transaction.atomic():
            capacitacion: Servicio = super().save(commit=False)
            id_empresa = self.request.user.empresa_id
            empresa = Empresa.objects.get(pk=id_empresa)
            try:
                horario_a_escoger = traer_horarios_disponibles_de_profesional(
                    id_profesional=empresa.profesional_asignado_id
                )[0]
            except IndexError:
                raise ValidationError(
                    "El profesional asignado no tiene horarios disponibles"
                )
            capacitacion.tipo = TiposDeServicio.CAPACITACION
            capacitacion.profesional_id = empresa.profesional_asignado_id
            capacitacion.empresa_id = empresa.id
            capacitacion.agendado_para = (
                arrow.get(
                    datetime.datetime.combine(
                        date=horario_a_escoger.fecha_inicio,
                        time=horario_a_escoger.desde,
                    )
                )
                .to("UTC")
                .datetime
            )
            capacitacion.duracion = datetime.timedelta(
                hours=duracion_en_hrs_por_servicio[TiposDeServicio.CAPACITACION]
            )
            capacitacion.save()
            factura_mensual: FacturaMensual = FacturaMensual.objects.filter(
                contrato__empresa=empresa
            ).last()
            factura_mensual.agregar_nueva_capacitacion(
                capacitacion=capacitacion, generado_por=self.request.user.id
            )
        return capacitacion


class ActualizarParticipanteCapacitacionForm(ModelForm):
    class Meta:
        model = Participante
        fields = ("rut", "nombre", "email")


class ActualizarParticipantesFormSetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form_method = "post"
        self.render_required_fields = True
        self.layout = Layout(
            Fieldset("Participante #{{forloop.counter}}"), "rut", "nombre", "email"
        )


class SolicitarVisitaForm(ModelForm):
    class Meta:
        model = Servicio
        fields = ("motivo",)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super().__init__(*args, **kwargs)
        for fieldname in self.fields:
            self.fields[fieldname].required = True

    def save(self, commit: bool = True):
        with transaction.atomic():
            visita: Servicio = super().save(commit=False)
            id_empresa = self.request.user.empresa_id
            empresa = Empresa.objects.get(pk=id_empresa)
            try:
                horario_a_escoger = traer_horarios_disponibles_de_profesional(
                    id_profesional=empresa.profesional_asignado_id
                )[0]
            except IndexError:
                raise ValidationError(
                    "El profesional asignado no tiene horarios disponibles"
                )
            visita.tipo = TiposDeServicio.VISITA
            visita.profesional_id = empresa.profesional_asignado_id
            visita.empresa_id = empresa.id
            visita.agendado_para = (
                arrow.get(
                    datetime.datetime.combine(
                        date=horario_a_escoger.fecha_inicio,
                        time=horario_a_escoger.desde,
                    )
                )
                .to("UTC")
                .datetime
            )
            visita.duracion = datetime.timedelta(
                hours=duracion_en_hrs_por_servicio[TiposDeServicio.VISITA]
            )
            visita.save()
            checklist_base: ChecklistBase = ChecklistBase.objects.filter(
                empresa_id=id_empresa
            ).last()
            Checklist.objects.create(items=checklist_base.items, servicio=visita)
            factura_mensual: FacturaMensual = FacturaMensual.objects.filter(
                contrato__empresa=empresa
            ).last()
            factura_mensual.agregar_nueva_visita(
                visita=visita, generado_por=self.request.user.id
            )
        return visita


class SolicitarAsesoriaForm(ModelForm):
    class Meta:
        model = Servicio
        fields = ("motivo",)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super().__init__(*args, **kwargs)
        for fieldname in self.fields:
            self.fields[fieldname].required = True

    def save(self, commit: bool = True):
        with transaction.atomic():
            asesoria: Servicio = super().save(commit=False)
            id_empresa = self.request.user.empresa_id
            empresa = Empresa.objects.get(pk=id_empresa)
            try:
                horario_a_escoger = traer_horarios_disponibles_de_profesional(
                    id_profesional=empresa.profesional_asignado_id
                )[0]
            except IndexError:
                raise ValidationError(
                    "El profesional asignado no tiene horarios disponibles"
                )
            asesoria.tipo = TiposDeServicio.ASESORIA_FISCALIZACION
            asesoria.profesional_id = empresa.profesional_asignado_id
            asesoria.empresa_id = empresa.id
            asesoria.agendado_para = (
                arrow.get(
                    datetime.datetime.combine(
                        date=horario_a_escoger.fecha_inicio,
                        time=horario_a_escoger.desde,
                    )
                )
                .to("UTC")
                .datetime
            )
            asesoria.duracion = datetime.timedelta(
                hours=duracion_en_hrs_por_servicio[
                    TiposDeServicio.ASESORIA_FISCALIZACION
                ]
            )
            asesoria.save()
            factura_mensual: FacturaMensual = FacturaMensual.objects.filter(
                contrato__empresa=empresa
            ).last()
            factura_mensual.agregar_nueva_asesoria(
                asesoria=asesoria, generado_por=self.request.user.id
            )
        return asesoria


class ActualizarMultaAsesoriaForm(ModelForm):
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
        self.id_servicio = kwargs.pop("id_servicio")

        super().__init__(*args, **kwargs)

    def save(self, commit: bool = True):
        self.instance.tipo = "MULTA"
        self.instance.servicio_id = self.id_servicio
        evento = super().save(commit=commit)
        return evento
