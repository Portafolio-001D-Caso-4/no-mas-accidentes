from django.urls import path

from no_mas_accidentes.profesionales.views import home_view

app_name = "profesionales"
urlpatterns = [
    path("home/", view=home_view, name="home"),
]
