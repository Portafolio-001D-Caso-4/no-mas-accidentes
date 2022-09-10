from datetime import time

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


class Contrato(models.Model):
    max_visitas_mensuales = models.PositiveIntegerField(
        default=2, validators=[MaxValueValidator(100)]
    )
    max_capacitaciones_mensuales = models.PositiveIntegerField(
        default=2, validators=[MaxValueValidator(100)]
    )
    max_asesorias_mensuales = models.PositiveIntegerField(
        default=10, validators=[MaxValueValidator(100)]
    )
    inicio_horario_llamadas = models.TimeField(default=time(hour=9, minute=0))
    fin_horario_llamadas = models.TimeField(default=time(hour=18, minute=0))
    max_actualizaciones_mensuales_reporte_cliente = models.PositiveIntegerField(
        default=1, validators=[MaxValueValidator(100)]
    )
    max_actualizaciones_checklist_anuales = models.PositiveIntegerField(
        default=2, validators=[MaxValueValidator(100)]
    )

    dia_facturacion = models.PositiveIntegerField(
        default=28, validators=[MaxValueValidator(28)]
    )

    valor_visita_extra = models.PositiveIntegerField(
        default=50_000, validators=[MaxValueValidator(1_000_000)]
    )
    valor_capacitacion_extra = models.PositiveIntegerField(
        default=100_000, validators=[MaxValueValidator(1_000_000)]
    )
    valor_asesoria_extra = models.PositiveIntegerField(
        default=100_000, validators=[MaxValueValidator(1_000_000)]
    )
    valor_llamada_fuera_horario = models.PositiveIntegerField(
        default=10_000, validators=[MaxValueValidator(1_000_000)]
    )
    valor_modificacion_checklist_extra = models.PositiveIntegerField(
        default=20_000, validators=[MaxValueValidator(1_000_000)]
    )
    valor_modificacion_reporte_extra = models.PositiveIntegerField(
        default=20_000, validators=[MaxValueValidator(1_000_000)]
    )
    valor_base = models.PositiveIntegerField(
        default=500_000, validators=[MaxValueValidator(10_000_000)]
    )

    esta_activo = models.BooleanField(default=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    archivo = models.FileField(upload_to="contratos/", null=True, blank=True)
    empresa = models.ForeignKey(Empresa, null=True, on_delete=models.SET_NULL)


class FacturaMensual(models.Model):
    expiracion = models.DateField()
    total = models.PositiveIntegerField(validators=[MaxValueValidator(100_000_000)])
    num_capacitaciones = models.PositiveIntegerField(
        validators=[MaxValueValidator(1_000)]
    )
    num_capacitaciones_extra = models.PositiveIntegerField(
        validators=[MaxValueValidator(1_000)]
    )
    num_visitas = models.PositiveIntegerField(validators=[MaxValueValidator(1_000)])
    num_visitas_extra = models.PositiveIntegerField(
        validators=[MaxValueValidator(1_000)]
    )
    num_asesorias = models.PositiveIntegerField(validators=[MaxValueValidator(1_000)])
    num_asesorias_extra = models.PositiveIntegerField(
        validators=[MaxValueValidator(1_000)]
    )
    num_llamadas = models.PositiveIntegerField(validators=[MaxValueValidator(1_000)])
    num_llamadas_fuera_horario = models.PositiveIntegerField(
        validators=[MaxValueValidator(1_000)]
    )
    num_modificaciones_checklist = models.PositiveIntegerField(
        validators=[MaxValueValidator(100)]
    )
    num_modificaciones_checklist_extra = models.PositiveIntegerField(
        validators=[MaxValueValidator(100)]
    )
    num_modificaciones_reporte = models.PositiveIntegerField(
        validators=[MaxValueValidator(100)]
    )
    num_modificaciones_reporte_extra = models.PositiveIntegerField(
        validators=[MaxValueValidator(100)]
    )

    forma_pago = models.CharField(max_length=100)
    es_pagado = models.BooleanField(default=False, blank=True)
    contrato = models.ForeignKey(Contrato, null=True, on_delete=models.SET_NULL)
    generado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)
    pagado_por = models.ForeignKey(
        "users.User", null=True, blank=True, on_delete=models.SET_NULL
    )
