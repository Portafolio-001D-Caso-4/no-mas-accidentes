from django.urls import path

from no_mas_accidentes.administracion.views import home_view

app_name = "administracion"
urlpatterns = [
    path("home/", view=home_view, name="home"),
]
