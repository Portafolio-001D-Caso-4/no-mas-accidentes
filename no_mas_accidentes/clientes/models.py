from datetime import time

from django.core.validators import (
    FileExtensionValidator,
    MaxValueValidator,
    MinValueValidator,
)
from django.db import models
from user_messages import api as message_user

from no_mas_accidentes.users import validators as users_validators
from no_mas_accidentes.users.models import User


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
    archivo = models.FileField(
        upload_to="contratos/",
        null=True,
        blank=True,
        validators=[FileExtensionValidator(allowed_extensions=["pdf"])],
    )
    empresa = models.ForeignKey(Empresa, null=True, on_delete=models.SET_NULL)


class FacturaMensual(models.Model):
    expiracion = models.DateField()
    total = models.PositiveIntegerField(
        validators=[MaxValueValidator(100_000_000)], default=0
    )
    num_capacitaciones = models.PositiveIntegerField(
        validators=[MaxValueValidator(1_000)], default=0
    )
    num_capacitaciones_extra = models.PositiveIntegerField(
        validators=[MaxValueValidator(1_000)], default=0
    )
    num_visitas = models.PositiveIntegerField(
        validators=[MaxValueValidator(1_000)], default=0
    )
    num_visitas_extra = models.PositiveIntegerField(
        validators=[MaxValueValidator(1_000)], default=0
    )
    num_asesorias = models.PositiveIntegerField(
        validators=[MaxValueValidator(1_000)], default=0
    )
    num_asesorias_extra = models.PositiveIntegerField(
        validators=[MaxValueValidator(1_000)], default=0
    )
    num_llamadas = models.PositiveIntegerField(
        validators=[MaxValueValidator(1_000)], default=0
    )
    num_llamadas_fuera_horario = models.PositiveIntegerField(
        validators=[MaxValueValidator(1_000)], default=0
    )
    num_modificaciones_checklist = models.PositiveIntegerField(
        validators=[MaxValueValidator(100)], default=0
    )
    num_modificaciones_checklist_extra = models.PositiveIntegerField(
        validators=[MaxValueValidator(100)], default=0
    )
    num_modificaciones_reporte = models.PositiveIntegerField(
        validators=[MaxValueValidator(100)], default=0
    )
    num_modificaciones_reporte_extra = models.PositiveIntegerField(
        validators=[MaxValueValidator(100)], default=0
    )

    forma_pago = models.CharField(max_length=100)
    es_pagado = models.BooleanField(default=False, blank=True)
    contrato = models.ForeignKey(Contrato, null=True, on_delete=models.SET_NULL)
    generado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)
    pagado_por = models.ForeignKey(
        "users.User", null=True, blank=True, on_delete=models.SET_NULL
    )

    @property
    def valor_capacitaciones_extra(self):
        return self.num_capacitaciones_extra * self.contrato.valor_capacitacion_extra

    @property
    def valor_visitas_extra(self):
        return self.num_visitas_extra * self.contrato.valor_visita_extra

    @property
    def valor_asesorias_extra(self):
        return self.num_asesorias_extra * self.contrato.valor_asesoria_extra

    @property
    def valor_llamadas_fuera_horario(self):
        return (
            self.num_llamadas_fuera_horario * self.contrato.valor_llamada_fuera_horario
        )

    @property
    def valor_modificaciones_checklist_extra(self):
        return (
            self.num_modificaciones_checklist_extra
            * self.contrato.valor_modificacion_checklist_extra
        )

    @property
    def valor_modificaciones_reporte_extra(self):
        return (
            self.num_modificaciones_reporte_extra
            * self.contrato.valor_modificacion_reporte_extra
        )

    def enviar_alerta_nuevo_cobro(self, mensaje: str, generado_por: int):
        mensaje_base = "Se ha generado un nuevo servicio: "
        mensaje_a_enviar = mensaje_base + mensaje
        if generado_por:
            mensaje_a_enviar += (
                f" Solicitado por {User.objects.get(id=generado_por).name}"
            )
        for usuario in self.contrato.empresa.user_set.all():
            message_user.info(usuario, mensaje_a_enviar)

    def agregar_nueva_capacitacion(self, capacitacion, generado_por: int):
        max_capacitaciones_mensuales = self.contrato.max_capacitaciones_mensuales
        if self.num_capacitaciones < max_capacitaciones_mensuales:
            original = self.num_capacitaciones
            self.enviar_alerta_nuevo_cobro(
                mensaje=f"Capacitación ({original+1} de {max_capacitaciones_mensuales} gratis)",
                generado_por=generado_por,
            )
        else:
            original = self.num_capacitaciones_extra
            self.enviar_alerta_nuevo_cobro(
                mensaje=f"Capacitación extra (${self.valor_capacitaciones_extra})",
                generado_por=generado_por,
            )
        original += 1
        self.total += self.valor_capacitaciones_extra
        self.save()

    def agregar_nueva_visita(self, visita, generado_por: int):
        max_visitas_mensuales = self.contrato.max_visitas_mensuales
        if self.num_visitas < max_visitas_mensuales:
            self.num_visitas += 1
            self.enviar_alerta_nuevo_cobro(
                mensaje=f"Visita ({self.num_visitas} de {max_visitas_mensuales} gratis)",
                generado_por=generado_por,
            )
        else:
            self.num_visitas_extra += 1
            self.enviar_alerta_nuevo_cobro(
                mensaje=f"Visita extra (${self.valor_visitas_extra})",
                generado_por=generado_por,
            )
        self.total += self.valor_visitas_extra
        self.save()

    def agregar_nueva_asesoria(self, asesoria, generado_por: int):
        max_asesorias_mensuales = self.contrato.max_asesorias_mensuales
        if self.num_asesorias < max_asesorias_mensuales:
            self.num_asesorias += 1
            self.enviar_alerta_nuevo_cobro(
                mensaje=f"Asesoría ({self.num_asesorias} de {max_asesorias_mensuales} gratis)",
                generado_por=generado_por,
            )
        else:
            self.num_asesorias_extra += 1
            self.enviar_alerta_nuevo_cobro(
                mensaje=f"Asesoría extra (${self.valor_asesorias_extra})",
                generado_por=generado_por,
            )
        self.total += self.valor_asesorias_extra
        self.save()

    def agregar_nueva_llamada(self, llamada, generado_por: int):
        # TODO: hacer logica por horario
        self.enviar_alerta_nuevo_cobro(mensaje="Llamada", generado_por=generado_por)

    def agregar_nueva_modificacion_checklist(self, checklist_base, generado_por: int):
        # TODO: hacer logica por año
        self.enviar_alerta_nuevo_cobro(
            mensaje="Modificicación checklist", generado_por=generado_por
        )

    def agregar_nueva_modificacion_reporte(self, generado_por: int):
        # TODO: hacer logica por año

        self.enviar_alerta_nuevo_cobro(
            mensaje="Modificación reporte", generado_por=generado_por
        )
