from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import AbstractUser


def usuario_es_administrador(user: AbstractUser) -> bool:
    return user.groups.filter(name="administrador").exists()


class EsAdministradorMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return usuario_es_administrador(self.request.user)


class PassRequestToFormViewMixin:
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs
