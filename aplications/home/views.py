from django.shortcuts import render
from django.views.generic import TemplateView
# Create your views here.

class IndexView(TemplateView) :
    template_name = 'base.html'

class AboutView(TemplateView) :
    template_name = 'about/about.html'