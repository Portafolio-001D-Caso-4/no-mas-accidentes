from django.db import models

from no_mas_accidentes.users import validators as users_validators


class Empresa(models.Model):
    rut = models.CharField(
        max_length=9, unique=True, validators=[users_validators.validar_rut]
    )
    giro = models.CharField(max_length=254)
    direccion = models.TextField()
    latitud = models.FloatField(blank=True, null=True)
    longitud = models.FloatField(blank=True, null=True)
    esta_activa = models.BooleanField(default=True)
