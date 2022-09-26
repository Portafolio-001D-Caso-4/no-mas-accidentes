from collections import Counter

from django import forms
from django.contrib import messages
from django.core.validators import MaxValueValidator, MinValueValidator

from no_mas_accidentes.clientes.models import FacturaMensual
from no_mas_accidentes.servicios.models import ChecklistBase


class CrearOActualizarChecklistBaseForm(forms.Form):
    numero_de_items = forms.IntegerField(
        widget=forms.HiddenInput(),
        validators=[MinValueValidator(3), MaxValueValidator(15)],
    )

    def __init__(self, *args, **kwargs):
        numero_de_items = kwargs.pop("numero_de_items", 3)
        self.id_empresa = kwargs.pop("id_empresa")
        self.request = kwargs.pop("request")
        super().__init__(*args, **kwargs)
        self.fields["numero_de_items"].initial = numero_de_items
        for index in range(int(numero_de_items)):
            self.fields[f"item_{index+1}"] = forms.CharField(
                min_length=10, max_length=256
            )

    def clean(self):
        cleaned_data = self.cleaned_data
        preguntas = list(self.cleaned_data.values())
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
        items_nuevos = {
            field: False for key, field in cleaned_data.items() if "item" in key
        }
        if self.initial:
            # actualizado
            checklist = ChecklistBase.objects.get(empresa_id=self.id_empresa)
            if checklist.items == items_nuevos:
                messages.info(
                    request=self.request,
                    message="Los items a actualizar son iguales a los anteriores, no se ha actualizado el checklist.",
                )
                return
            messages.success(
                request=self.request, message="Se ha actualizado el checklist"
            )
            factura_mensual: FacturaMensual = FacturaMensual.objects.last()
            factura_mensual.agregar_nueva_modificacion_checklist(
                checklist_base=checklist, generado_por=self.request.user.id
            )
            checklist.items = items_nuevos
            checklist.save()
        else:
            # creado
            checklist = ChecklistBase(items=items_nuevos, empresa_id=self.id_empresa)
            messages.success(request=self.request, message="Se ha creado el checklist")
        checklist.save()
