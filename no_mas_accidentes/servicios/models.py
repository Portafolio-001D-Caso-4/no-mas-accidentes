from django.core.validators import MaxValueValidator
from django.db import models

from no_mas_accidentes.clientes.models import Empresa
from no_mas_accidentes.profesionales.models import Profesional
from no_mas_accidentes.users import validators


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
    duracion = models.DurationField(null=True, blank=True)


class OportunidadDeMejora(models.Model):
    creado_en = models.DateTimeField(auto_now_add=True)
    contenido = models.TextField()

    realizado = models.BooleanField(null=True, default=None)
    revisado_en = models.DateTimeField(null=True, blank=True)
    revisado_por = models.ForeignKey(
        Profesional, null=True, blank=True, on_delete=models.SET_NULL
    )
    servicio = models.ForeignKey(Servicio, null=True, on_delete=models.SET_NULL)


class Evento(models.Model):
    TIPOS = [
        ("ACCIDENTE", "ACCIDENTE"),
        ("MULTA", "MULTA"),
    ]
    tipo = models.CharField(choices=TIPOS, max_length=256)
    fecha = models.DateTimeField()
    contenido = models.TextField()

    creado_en = models.DateTimeField(auto_now_add=True)
    servicio = models.ForeignKey(Servicio, null=True, on_delete=models.SET_NULL)


class ChecklistBase(models.Model):
    items = models.JSONField()  # pregunta: respuesta
    empresa = models.ForeignKey(Empresa, null=True, on_delete=models.SET_NULL)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)


class Checklist(models.Model):
    items = models.JSONField()  # pregunta: respuesta
    actualizado_en = models.DateTimeField(auto_now=True)
    aplicado_en = models.DateTimeField(auto_now_add=True)
    servicio = models.OneToOneField(Servicio, null=True, on_delete=models.SET_NULL)


class Participante(models.Model):
    nombre = models.CharField(max_length=255)
    email = models.EmailField()
    rut = models.CharField(
        max_length=9, unique=True, validators=[validators.validar_rut]
    )
    asiste = models.BooleanField(default=False)
    servicio = models.ForeignKey(Servicio, null=True, on_delete=models.SET_NULL)
