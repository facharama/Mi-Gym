# aplications/usuarios/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test

from .utils import is_admin, is_socio
from .decorators import role_required
from .forms import UserCreateWithRoleForm


@login_required
@user_passes_test(lambda u: u.is_staff or u.is_superuser)
def crear_usuario(request):
    if request.method == "POST":
        form = UserCreateWithRoleForm(request.POST)
        if form.is_valid():
            user = form.save()

            # Si existe el modelo Socio y el rol elegido fue Socio, crear perfil
            try:
                from aplications.socios.models import Socio  # ajustá si tu modelo se llama distinto
                if form.cleaned_data["rol"] == "Socio":
                    Socio.objects.get_or_create(user=user)
            except Exception:
                # Si no existe el modelo Socio, lo ignoramos
                pass

            return redirect("admin_dashboard")  # o a donde prefieras
    else:
        form = UserCreateWithRoleForm()

    return render(request, "usuarios/crear_usuario.html", {"form": form})


@login_required
def role_redirect(request):
    """Decide a qué dashboard ir después del login."""
    if is_admin(request.user):
        return redirect("admin_dashboard")
    if is_socio(request.user):
        return redirect("socio_dashboard")
    return redirect("login")  # o a una vista "sin rol"


@login_required
@role_required("Administrador")
def admin_dashboard(request):
    data = {
        "total_socios": 0,
        "cuotas_pendientes": 0,
        "ocupacion_actual": 0,
    }
    # 👉 usa una plantilla NAMESPACEADA para evitar que Django agarre otra
    return render(request, "usuarios/admin_dashboard.html", data)



@login_required
@role_required("Socio")
def socio_dashboard(request):
    data = {
        "estado_cuota": "paga",
        "rutina_hoy": [],
        "ocupacion_actual": 0,
    }
    return render(request, "dash/socio_dashboard.html", data)

