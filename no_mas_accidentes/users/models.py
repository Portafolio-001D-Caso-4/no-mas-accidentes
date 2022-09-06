from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from no_mas_accidentes.users import validators


class User(AbstractUser):
    """
    Default custom user model for no-mas-accidentes.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    #: First and last name do not cover name patterns around the globe
    name = models.CharField(_("Nombre"), max_length=255)
    first_name = None  # type: ignore
    last_name = None  # type: ignore
    email = models.EmailField(_("email address"), unique=True)
    rut = models.CharField(
        max_length=9, unique=True, validators=[validators.validar_rut]
    )
    empresa = models.ForeignKey(
        "clientes.Empresa", blank=True, null=True, on_delete=models.SET_NULL
    )

    def get_absolute_url(self):
        """Get url for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})
