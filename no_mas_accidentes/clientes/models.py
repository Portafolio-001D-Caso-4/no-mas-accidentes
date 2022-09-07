from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from no_mas_accidentes.users import validators as users_validators


class Empresa(models.Model):
    rut = models.CharField(
        max_length=9, unique=True, validators=[users_validators.validar_rut]
    )
    nombre = models.CharField(max_length=254)
    giro = models.CharField(max_length=254)
    direccion = models.TextField()
    latitud = models.FloatField(blank=True, null=True)
    longitud = models.FloatField(blank=True, null=True)
    esta_activa = models.BooleanField(default=True)
    telefono = models.PositiveIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(900000000), MaxValueValidator(999999999)],
    )
    profesional_asignado = models.ForeignKey(
        "profesionales.Profesional", blank=True, null=True, on_delete=models.SET_NULL
    )

    def __str__(self):
        return f"{self.rut} - {self.nombre}"
