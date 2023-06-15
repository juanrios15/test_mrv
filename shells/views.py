from django.shortcuts import render
from django.views.generic import View
from django.views.generic.list import ListView
from django.template.response import TemplateResponse

from .models import Category


class CategoriesListView(ListView):
    model = Category
    paginate_by = 100
    template_name = "config_session.html"


class StartTrainingView(View):
    template_name = "start_training.html"

    def get(self, request, *args, **kwargs):
        form_data = request.GET.dict()
        for param, value in form_data.items():
            print(f"Parámetro: {param}, Valor: {value}")

        return TemplateResponse(request, "start_training.html")
