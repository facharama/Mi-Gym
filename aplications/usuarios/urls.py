from django.urls import path
from . import views as uviews
from .views import crear_usuario

urlpatterns = [
    path("post-login/", uviews.role_redirect, name="role_redirect"),
    path("dashboard/admin/", uviews.admin_dashboard, name="admin_dashboard"),
    path("dashboard/socio/", uviews.socio_dashboard, name="socio_dashboard"),
    path("nuevo/", crear_usuario, name="usuarios_crear"),
]
