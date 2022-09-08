from django.contrib import admin

from no_mas_accidentes.clientes.models import Contrato, Empresa


@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = ["rut", "nombre", "giro", "esta_activa"]


@admin.register(Contrato)
class ContratoAdmin(admin.ModelAdmin):
    list_display = ["id", "creado_en", "esta_activo"]
