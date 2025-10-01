from django.contrib.auth.decorators import login_required
from django.db.models import Subquery, OuterRef, Count, Sum, Value, IntegerField
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseNotAllowed
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from .forms import AccesoForm
from .models import Acceso
from aplications.socios.models import Sucursal, Socio 

from django.db.models.functions import Coalesce 
# ---------------------------
# Alta manual con formulario
# ---------------------------
@login_required
def registrar_acceso(request):
    if request.method == "POST":
        form = AccesoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("ocupacion:ocupacion_actual")  # usa namespace si lo tenés
    else:
        form = AccesoForm()
    return render(request, "ocupacion/form_acceso.html", {"form": form})

# --------------------------------------
# Vista HTML para ver ocupación por sede
# --------------------------------------
@login_required
def ocupacion_actual(request):
    """
    Lógica: por cada socio en cada sucursal, tomamos su último movimiento.
    Si el último es 'Ingreso' => está adentro.
    Optimizado con Subquery (evita N+1 queries).
    """
    # Subconsulta: para cada (socio, sucursal), traemos el TIPO del último movimiento
    ultimo_tipo_subq = (
        Acceso.objects
        .filter(socio_id=OuterRef("socio_id"), sucursal_id=OuterRef("sucursal_id"))
        .order_by("-fecha_hora")
        .values("tipo")[:1]
    )

    # Filtramos solo los casos cuyo último movimiento fue 'Ingreso'
    ultimos_ingreso = (
        Acceso.objects
        .values("socio_id", "sucursal_id")
        .distinct()
        .annotate(ultimo_tipo=Subquery(ultimo_tipo_subq))
        .filter(ultimo_tipo="Ingreso")
    )

    # Conteo por sucursal
    conteo_por_sucursal = (
        ultimos_ingreso
        .values("sucursal_id")
        .annotate(dentro=Count("socio_id"))
    )
    dentro_map = {row["sucursal_id"]: row["dentro"] for row in conteo_por_sucursal}

    # Armamos respuesta para cada sucursal
    data = []
    for s in Sucursal.objects.all():
        occ = dentro_map.get(s.id, 0)
        cap = getattr(s, "aforo_maximo", None) or 0
        pct = (occ * 100.0 / cap) if cap else 0.0

        # Umbrales (asumimos que existen en Sucursal; si no, fijá valores por defecto)
        low = getattr(s, "umbral_bajo_pct", 33)
        mid = getattr(s, "umbral_medio_pct", 66)

        if pct <= low:
            leyenda = "Baja"
        elif pct <= mid:
            leyenda = "Media"
        else:
            leyenda = "Alta"

        data.append({"sucursal": s, "ocupacion": occ, "capacidad": cap, "porcentaje": round(pct, 1), "leyenda": leyenda})

    return render(request, "ocupacion/actual.html", {"items": data})

# ---------------------------
# Página del simulador visual
# ---------------------------
@login_required
def simulador(request):
    return render(request, "ocupacion/simulador.html")

# -------------------------------------------------------------------
# API para el simulador: registrar IN/OUT y consultar ocupación actual
# (Django puro, sin DRF; si usás DRF, lo migramos fácil más adelante)
# -------------------------------------------------------------------

@csrf_exempt
def access_event(request):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])

    import json, traceback
    try:
        data = json.loads(request.body.decode("utf-8"))
    except Exception:
        return JsonResponse({"detail": "invalid json"}, status=400)

    member_code = data.get("member_code")
    atype = data.get("type")  # IN / OUT
    sucursal_id = data.get("sucursal_id")

    if not member_code or atype not in ("IN", "OUT"):
        return JsonResponse({"detail": "member_code y type son obligatorios (IN/OUT)"}, status=400)

    # 1) Buscar socio por DNI, fallback username
    from aplications.socios.models import Socio, Sucursal
    try:
        socio = Socio.objects.get(dni=member_code)
    except Socio.DoesNotExist:
        try:
            socio = Socio.objects.get(user__username=member_code)
        except Socio.DoesNotExist:
            return JsonResponse({"detail": "member not found (dni/username)"}, status=404)

    # 2) Resolver sucursal
    sucursal = None
    if sucursal_id:
        sucursal = Sucursal.objects.filter(pk=sucursal_id).first()
    if not sucursal:
        sucursal = getattr(socio, "sucursal", None) or Sucursal.objects.first()
    if not sucursal:
        return JsonResponse({"detail": "no hay sucursal disponible (creá una en /admin)"}, status=400)

    # 3) Crear movimiento
    try:
        from django.utils import timezone
        from .models import Acceso
        tipo = "Ingreso" if atype == "IN" else "Egreso"
        Acceso.objects.create(
            socio=socio,
            sucursal=sucursal,
            tipo=tipo,
            fecha_hora=timezone.now()
        )
        return JsonResponse({"status": "ok"})
    except Exception as e:
        # Log y respuesta clara
        traceback.print_exc()
        return JsonResponse({"detail": f"server error: {e}"}, status=500)




def occupancy_current(request):
    """
    Devuelve ocupación y capacidad.
    - ?sucursal_id=1 -> cuenta y capacidad de esa sucursal
    - sin sucursal_id -> cuenta total y capacidad total (suma de aforos)
    Respuesta: { "count": N, "capacity": M, "sucursal_id": "..." }
    """
    sucursal_id = request.GET.get("sucursal_id")

    # Subconsulta: último tipo (Ingreso/Egreso) por (socio, sucursal)
    ultimo_tipo_subq = (
        Acceso.objects
        .filter(socio_id=OuterRef("socio_id"), sucursal_id=OuterRef("sucursal_id"))
        .order_by("-fecha_hora")
        .values("tipo")[:1]
    )

    # Base: sólo los que su último movimiento fue "Ingreso"
    base = (
        Acceso.objects
        .values("socio_id", "sucursal_id")
        .distinct()
        .annotate(ultimo_tipo=Subquery(ultimo_tipo_subq))
        .filter(ultimo_tipo="Ingreso")
    )

    # Filtrado opcional por sucursal
    if sucursal_id:
        base = base.filter(sucursal_id=sucursal_id)

    count = base.values("socio_id").count()

    # ---- capacidad ----
    # Si viene sucursal_id: devolver aforo de esa sucursal
    # Si no: sumar aforo de todas
    from aplications.socios.models import Sucursal

    if sucursal_id:
        suc = Sucursal.objects.filter(pk=sucursal_id).values("aforo_maximo").first()
        capacity = int((suc or {}).get("aforo_maximo") or 0)
    else:
        agg = Sucursal.objects.aggregate(
            total=Coalesce(Sum("aforo_maximo"), Value(0, output_field=IntegerField()))
        )
        capacity = int(agg["total"] or 0)

    return JsonResponse({
        "count": count,
        "capacity": capacity,
        "sucursal_id": sucursal_id or None,
    })
