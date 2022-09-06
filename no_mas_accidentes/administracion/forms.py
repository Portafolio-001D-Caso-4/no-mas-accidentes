from django.contrib.auth.models import Group
from django.forms import ModelForm

from no_mas_accidentes.users.models import User


class CrearClienteForm(ModelForm):
    class Meta:
        model = User
        fields = ("rut", "username", "email", "name")

    def save(self, commit: bool = True):
        cliente = super().save(commit=False)
        cliente.rut = str(cliente.rut).upper()
        cliente.save()
        grupo = Group.objects.get(name="cliente")
        cliente.groups.add(grupo)
        return cliente


class ActualizarDetalleClienteForm(ModelForm):
    class Meta:
        model = User
        fields = ("rut", "username", "email", "name")
