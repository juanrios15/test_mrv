import math
import random

from django.shortcuts import render
from django.views.generic import View
from django.views.generic.list import ListView
from django.template.response import TemplateResponse

from .models import Category, Shell


class CategoriesListView(ListView):
    model = Category
    template_name = "config_session.html"


class StartTrainingView(View):
    template_name = "start_training.html"

    def post(self, request, *args, **kwargs):
        form_data = request.POST.dict()
        shell_count = int(form_data["total_cards"])
        # Getting hard shells count
        hard_count = math.floor(shell_count / 3)
        easy_count = shell_count - hard_count
        ids = [int(valor) for clave, valor in form_data.items() if clave not in ["total_cards", "csrfmiddlewaretoken"]]
        # Filtering easy and hard shells
        if len(ids) == 0:
            # If there is no selected categories, get all
            candidate_easy_shells = (
                Shell.objects.filter(difficulty_level__value=1).order_by("?").values_list("id", flat=True)
            )
            candidate_hard_shells = (
                Shell.objects.filter(difficulty_level__value__gt=1).order_by("?").values_list("id", flat=True)
            )
        else:
            candidate_easy_shells = (
                Shell.objects.filter(category__in=ids, difficulty_level__value=1)
                .order_by("?")
                .values_list("id", flat=True)
            )
            candidate_hard_shells = (
                Shell.objects.filter(category__in=ids, difficulty_level__value__gt=1)
                .order_by("?")
                .values_list("id", flat=True)
            )
        # Selecting desired amount
        hard_shells_ids = candidate_hard_shells[:hard_count]
        easy_shells_ids = candidate_easy_shells[:easy_count]
        # Getting hard shells and hardest shell
        hard_shells = Shell.objects.filter(id__in=hard_shells_ids).order_by("-difficulty_level__value")
        last_shell = hard_shells.first()
        # Get session shells in random order
        session_shells = Shell.objects.filter(id__in=list(hard_shells_ids) + list(easy_shells_ids)).exclude(
            id=last_shell.id
        ).order_by("?")
        print("Session shells:")
        for shell in session_shells:
            print(shell.title, ",", shell.difficulty_level, ",", shell.category)
        print("Last Shell:")
        print(last_shell.title, last_shell.difficulty_level, last_shell.category)

        return TemplateResponse(request, "start_training.html")
