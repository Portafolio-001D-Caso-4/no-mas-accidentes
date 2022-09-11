from allauth.account.utils import send_email_confirmation
from django.contrib.auth.models import Group
from django.core.validators import MaxValueValidator, MinValueValidator
from django.forms import IntegerField, ModelForm, widgets

from no_mas_accidentes.clientes.models import Contrato, Empresa
from no_mas_accidentes.profesionales.models import Profesional
from no_mas_accidentes.users.models import User


class CrearClienteForm(ModelForm):
    class Meta:
        model = User
        fields = ("rut", "username", "name", "email", "empresa")

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super().__init__(*args, **kwargs)
        self.fields["rut"].help_text = "Sin guión ni puntos"
        self.fields["name"].help_text = "Nombre completo del cliente"

    def clean_rut(self):
        rut = str(self.cleaned_data["rut"]).upper()
        return rut

    def save(self, commit: bool = True):
        cliente = super().save(commit=False)
        cliente.rut = str(cliente.rut).upper()
        cliente.save()
        grupo = Group.objects.get(name="cliente")
        cliente.groups.add(grupo)
        send_email_confirmation(request=self.request, user=cliente)
        return cliente


class ActualizarDetalleClienteForm(ModelForm):
    class Meta:
        model = User
        fields = ("rut", "username", "email", "name", "empresa", "is_active")

    def __init__(self, *args, **kwargs):
        self.fields["name"].help_text = "Nombre completo del cliente"

    def clean_rut(self):
        rut = str(self.cleaned_data["rut"]).upper()
        return rut


class CrearProfesionalForm(ModelForm):
    telefono = IntegerField(
        label="Teléfono",
        widget=widgets.TextInput(attrs={"maxlength": 9}),
        validators=[MinValueValidator(900000000), MaxValueValidator(999999999)],
    )

    class Meta:
        model = User
        fields = ("rut", "username", "name", "email")

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super().__init__(*args, **kwargs)
        self.fields["rut"].help_text = "Sin guión ni puntos"
        self.fields["name"].help_text = "Nombre completo del profesional"

    def clean_rut(self):
        rut = str(self.cleaned_data["rut"]).upper()
        return rut

    def save(self, commit: bool = True):
        usuario = super().save(commit=False)
        if commit:
            usuario.save()
        profesional = Profesional(
            telefono=self.cleaned_data["telefono"], usuario=usuario
        )
        profesional.save()
        grupo = Group.objects.get(name="profesional")
        usuario.groups.add(grupo)
        send_email_confirmation(request=self.request, user=usuario)
        return usuario


class ActualizarDetalleProfesionalForm(ModelForm):
    telefono = IntegerField(
        label="Teléfono",
        widget=widgets.TextInput(attrs={"maxlength": 9}),
        validators=[MinValueValidator(900000000), MaxValueValidator(999999999)],
    )

    class Meta:
        model = User
        fields = (
            "rut",
            "username",
            "email",
            "name",
            "telefono",
            "is_active",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["telefono"].initial = self.instance.profesional.telefono
        self.fields["name"].help_text = "Nombre completo del profesional"

    def clean_rut(self):
        rut = str(self.cleaned_data["rut"]).upper()
        return rut

    def save(self, commit=True):
        usuario = super().save(commit=False)
        if commit:
            usuario.save()
        profesional = usuario.profesional
        profesional.telefono = self.cleaned_data["telefono"]
        profesional.save()
        return usuario


class CrearEmpresaForm(ModelForm):
    class Meta:
        model = Empresa
        fields = (
            "nombre",
            "rut",
            "giro",
            "direccion",
            "telefono",
            "profesional_asignado",
        )

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super().__init__(*args, **kwargs)
        self.fields["rut"].help_text = "Sin guión ni puntos"
        self.fields["direccion"].widget = widgets.TextInput()
        self.fields["telefono"].widget = widgets.TextInput(attrs={"maxlength": 9})

    def clean_rut(self):
        rut = str(self.cleaned_data["rut"]).upper()
        return rut

    def save(self, commit: bool = True):
        empresa = super().save(commit=False)
        if commit:
            empresa.save()
        Contrato.objects.create(empresa=empresa)
        return empresa


class ActualizarDetalleEmpresaForm(ModelForm):
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

    def clean_rut(self):
        rut = str(self.cleaned_data["rut"]).upper()
        return rut

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["rut"].help_text = "Sin guión ni puntos"
        self.fields["telefono"].label = "Teléfono"
        self.fields["telefono"].widget = widgets.TextInput(attrs={"maxlength": 9})
        self.fields["direccion"].label = "Dirección"
        self.fields["direccion"].widget = widgets.TextInput()


class ActualizarContratoForm(ModelForm):
    class Meta:
        model = Contrato
        fields = ("archivo",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["archivo"].required = True
        self.fields["archivo"].help_text = "Solo se aceptan formatos PDF"
