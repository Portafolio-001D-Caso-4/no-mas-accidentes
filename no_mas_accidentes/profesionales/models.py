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

    @property
    def porcentaje_accidentabilidad_historico(self):
        from no_mas_accidentes.profesionales.business_logic.accidentabilidad import (
            calcular_accidentabilidad_por_profesional,
        )

        return calcular_accidentabilidad_por_profesional(
            profesional_id=self.usuario.pk, historico=True
        )


class HorarioProfesional(models.Model):
    fecha_inicio = models.DateField()
    fecha_termino = models.DateField()
    desde = models.TimeField()
    hasta = models.TimeField()
    profesional = models.ForeignKey(Profesional, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return (
            f"{self.fecha_inicio} - {self.fecha_termino} - {self.desde} - {self.hasta}"
        )

    class Meta:
        unique_together = ["desde", "profesional", "fecha_inicio"]
