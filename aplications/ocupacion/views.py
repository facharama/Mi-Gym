from django.contrib.auth.decorators import login_required
from django.db.models import Max
from django.shortcuts import render, redirect
from .forms import AccesoForm
from .models import Acceso
from aplications.socios.models import Sucursal

# Create your views here.

@login_required
def registrar_acceso(request):
    if request.method == "POST":
        form = AccesoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("ocupacion_actual")
    else:
        form = AccesoForm()
    return render(request, "ocupacion/form_acceso.html", {"form": form})

@login_required
def ocupacion_actual(request):
    """Cálculo simple: por socio tomamos el último movimiento; si es Ingreso => dentro."""
    # último movimiento por socio
    ultimos = (Acceso.objects
               .values("socio_id", "sucursal_id")
               .annotate(ult=Max("fecha_hora")))
    # construir un set de (sucursal_id) con count
    dentro_por_sucursal = {}
    for u in ultimos:
        mov = Acceso.objects.filter(socio_id=u["socio_id"], sucursal_id=u["sucursal_id"], fecha_hora=u["ult"]).first()
        if mov and mov.tipo == "Ingreso":
            dentro_por_sucursal[mov.sucursal_id] = dentro_por_sucursal.get(mov.sucursal_id, 0) + 1

    sucursales = Sucursal.objects.all()
    data = []
    for s in sucursales:
        occ = dentro_por_sucursal.get(s.id, 0)
        if s.aforo_maximo:
            pct = (occ * 100.0) / s.aforo_maximo
        else:
            pct = 0
        if pct <= s.umbral_bajo_pct:
            leyenda = "Baja"
        elif pct <= s.umbral_medio_pct:
            leyenda = "Media"
        else:
            leyenda = "Alta"
        data.append({"sucursal": s, "ocupacion": occ, "leyenda": leyenda})

    return render(request, "ocupacion/actual.html", {"items": data})
