from django.contrib import admin
from django.urls import path, include
from aplications.home.views import IndexView,AboutView
from django.views.generic.base import RedirectView
from core.views import home, CustomLoginView, admin_dashboard, socios_dashboard
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view(), name='home'),
    path('login/', auth_views.LoginView.as_view(
        template_name='home/login.html'
    ), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('socios/dashboard/', socios_dashboard, name='socios'),
    path('socios/', include('aplications.socios.urls')),
    path('panel-admin/', admin_dashboard, name='panel_admin'),
    path('pagos/', include('aplications.pagos.urls')),
    path('rutina/', include('aplications.rutina.urls')),
    path('ocupacion/', include('aplications.ocupacion.urls')),
    path('about/', AboutView.as_view(), name='about'),
    path("usuarios/", include("aplications.usuarios.urls")),
    path('ckeditor5/', include('django_ckeditor_5.urls')),

]


