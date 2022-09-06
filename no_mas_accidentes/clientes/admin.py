from django.contrib import admin

from no_mas_accidentes.clientes.models import Empresa


@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = ["rut", "nombre", "giro", "esta_activa"]
