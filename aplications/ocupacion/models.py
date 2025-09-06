from django.db import models
from django.db import models
from aplications.socios.models import Socio, Sucursal
# Create your models here.

class Acceso(models.Model):
    """Registro de ingreso/egreso de un socio a una sucursal."""
    TIPOS = [("Ingreso", "Ingreso"), ("Egreso", "Egreso")]
    ORIGENES = [("Molturno", "Molturno"), ("Recepcion", "Recepción"), ("Manual", "Manual")]

    socio = models.ForeignKey(Socio, on_delete=models.CASCADE, related_name="accesos")
    sucursal = models.ForeignKey(Sucursal, on_delete=models.PROTECT, related_name="accesos")
    fecha_hora = models.DateTimeField(auto_now_add=True)
    tipo = models.CharField(max_length=10, choices=TIPOS)
    origen = models.CharField(max_length=20, choices=ORIGENES, default="Recepcion")

    class Meta:
        indexes = [
            models.Index(fields=["sucursal", "fecha_hora"]),
            models.Index(fields=["socio", "fecha_hora"]),
        ]
        ordering = ["-fecha_hora"]
        verbose_name = "Acceso"
        verbose_name_plural = "Accesos"

    def __str__(self):
        return f"{self.socio} - {self.tipo} @ {self.fecha_hora:%Y-%m-%d %H:%M}"