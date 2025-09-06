from django.contrib import admin
from django.urls import path, include
from aplications.home.views import IndexView,AboutView
from django.views.generic.base import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view() ),
    path("socios/", include("aplications.socios.urls")),
    path("pagos/", include("aplications.pagos.urls")),
    path("rutina/", include("aplications.rutina.urls")),
    path("ocupacion/", include("aplications.ocupacion.urls")),
    path('about', AboutView.as_view(), name='about'),
    path('ckeditor5/', include('django_ckeditor_5.urls')),

]
