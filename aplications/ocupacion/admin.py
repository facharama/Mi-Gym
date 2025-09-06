from django.contrib import admin
from .models import Acceso

# Register your models here.

@admin.register(Acceso)
class AccesoAdmin(admin.ModelAdmin):
    list_display = ("id", "socio", "sucursal", "tipo", "origen", "fecha_hora")
    search_fields = ("socio_userusername", "socio_dni")
    list_filter = ("sucursal", "tipo", "origen")
    ordering = ("-fecha_hora",)