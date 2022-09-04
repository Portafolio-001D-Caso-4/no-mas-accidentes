from django.urls import path

from no_mas_accidentes.clientes.views import home_view

app_name = "clientes"
urlpatterns = [
    path("home/", view=home_view, name="home"),
]
