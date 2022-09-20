from django.forms import ModelForm, widgets

from no_mas_accidentes.clientes.models import Empresa


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
