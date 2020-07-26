from django.shortcuts import render
from django.views.generic import TemplateView,ListView


class index(TemplateView):
    template_name = "index.html"
