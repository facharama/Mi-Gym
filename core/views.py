from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.views import LoginView
from .utils import in_group

# Create your views here.

def home(request):
    return render(request, "home.html")

class CustomLoginView(LoginView):
    template_name = "login.html"
    def get_success_url(self):
        u = self.request.user
        if u.is_staff:
            return "/admin/"        
        if in_group(u, "Socio"):
            return "/socios/"
        return "/"                    

@login_required
@user_passes_test(lambda u: u.is_staff)
def admin_dashboard(request):
    return render(request, "admin_dashboard.html")

@login_required
@user_passes_test(lambda u: in_group(u, "Socio"))
def socios_dashboard(request):
    return render(request, "socios_dashboard.html")
