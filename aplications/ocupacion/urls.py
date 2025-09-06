from django.urls import path
from . import views

app_name = "ocupacion"

urlpatterns = [
    path("registrar/", views.registrar_acceso, name="ocupacion_registrar"),
    path("actual/", views.ocupacion_actual, name="ocupacion_actual")
]