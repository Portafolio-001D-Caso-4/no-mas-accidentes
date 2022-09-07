from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from no_mas_accidentes.users.models import User


class Profesional(models.Model):
    usuario = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    telefono = models.PositiveIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(900000000), MaxValueValidator(999999999)],
    )

    def __str__(self):
        return f"{self.usuario.rut} - {self.usuario.name}"
