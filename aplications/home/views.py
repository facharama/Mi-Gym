from django.shortcuts import render
from django.views.generic import TemplateView
# Create your views here.

class IndexView(TemplateView) :
    template_name = 'home/index.html'

class AboutView(TemplateView) :
    template_name = 'about/about.html'