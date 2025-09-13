from django import forms
from .models import Socio, Suscripcion

class SocioForm(forms.ModelForm):
    class Meta:
        model = Socio
        fields = ["nombre", "apellido", "email", "dni", "sucursal", "estado"]


class SuscripcionForm(forms.ModelForm):
    class Meta:
        model = Suscripcion
        fields = ["socio", "plan", "fecha_inicio", "fecha_fin", "monto", "estado", "auto_renovacion"]
