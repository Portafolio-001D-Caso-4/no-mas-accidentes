from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from no_mas_accidentes.clientes.models import Empresa
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


class Servicio(models.Model):
    TIPOS = [
        ("ASESORIA EMERGENCIA", "ASESORIA EMERGENCIA"),
        ("ASESORIA FISCALIZACION ", "ASESORIA FISCALIZACION"),
        ("CAPACITACION", "CAPACITACION"),
        ("VISITA", "VISITA"),
        ("LLAMADA", "LLAMADA"),
    ]
    tipo = models.CharField(choices=TIPOS, max_length=256)
    profesional = models.ForeignKey(Profesional, null=True, on_delete=models.SET_NULL)
    empresa = models.ForeignKey(Empresa, null=True, on_delete=models.SET_NULL)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    agendado_para = models.DateTimeField(null=True, blank=True)
    realizado_en = models.DateTimeField(null=True, blank=True)
    num_participantes = models.PositiveIntegerField(
        null=True,
        blank=True,
        validators=[MaxValueValidator(10_000)],
    )
    motivo = models.TextField(null=True, blank=True)
    contenido = models.TextField(null=True, blank=True)
    materiales = models.TextField(null=True, blank=True)
