from allauth.account.utils import send_email_confirmation
from django.contrib.auth.models import Group
from django.core.validators import MaxValueValidator, MinValueValidator
from django.forms import IntegerField, ModelForm

from no_mas_accidentes.profesionales.models import Profesional
from no_mas_accidentes.users.models import User


class CrearClienteForm(ModelForm):
    class Meta:
        model = User
        fields = ("rut", "username", "email", "name", "empresa")

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super().__init__(*args, **kwargs)

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
        fields = ("rut", "username", "email", "name", "is_active", "empresa")

    def clean_rut(self):
        rut = str(self.cleaned_data["rut"]).upper()
        return rut


class CrearProfesionalForm(ModelForm):
    telefono = IntegerField(
        validators=[MinValueValidator(900000000), MaxValueValidator(999999999)],
    )

    class Meta:
        model = User
        fields = ("rut", "username", "email", "name")

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super().__init__(*args, **kwargs)

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
        validators=[MinValueValidator(900000000), MaxValueValidator(999999999)],
    )

    class Meta:
        model = User
        fields = (
            "rut",
            "username",
            "email",
            "name",
            "is_active",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["telefono"].initial = self.instance.profesional.telefono

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
