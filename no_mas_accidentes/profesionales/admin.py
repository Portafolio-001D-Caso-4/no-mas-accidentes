from django.contrib import admin

from no_mas_accidentes.profesionales.models import Profesional


@admin.register(Profesional)
class ProfesionalAdmin(admin.ModelAdmin):
    list_display = ["pk", "telefono"]
