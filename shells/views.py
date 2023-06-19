import math

from django.views.generic import View, DetailView
from django.views.generic.list import ListView
from django.shortcuts import redirect

from .models import Category, Shell, TrainingSession, UserShell


class CategoriesListView(ListView):
    model = Category
    template_name = "config_session.html"


class StartTrainingView(View):
    def post(self, request, *args, **kwargs):
        # TODO: set all checkboxes to 'checked' at start
        form_data = request.POST.dict()
        shell_count = int(form_data["total_cards"])
        # Getting hard shells count
        hard_count = math.floor(shell_count / 3)
        easy_count = shell_count - hard_count
        category_ids = [
            int(valor) for clave, valor in form_data.items() if clave not in ["total_cards", "csrfmiddlewaretoken"]
        ]
        # Filtering easy and hard shells
        if len(category_ids) == 0:
            # If there is no selected categories, get all
            candidate_easy_shells = (
                Shell.objects.filter(difficulty_level__value=1).order_by("?").values_list("id", flat=True)
            )
            candidate_hard_shells = (
                Shell.objects.filter(difficulty_level__value__gt=1).order_by("?").values_list("id", flat=True)
            )
        else:
            candidate_easy_shells = (
                Shell.objects.filter(category__in=category_ids, difficulty_level__value=1)
                .order_by("?")
                .values_list("id", flat=True)
            )
            candidate_hard_shells = (
                Shell.objects.filter(category__in=category_ids, difficulty_level__value__gt=1)
                .order_by("?")
                .values_list("id", flat=True)
            )
        # Selecting desired amount
        hard_shells_ids = list(candidate_hard_shells)[:hard_count]
        easy_shells_ids = list(candidate_easy_shells)[:easy_count]
        # # Getting hard shells and hardest shell
        last_shell_id = hard_shells_ids[0]
        available_ids = hard_shells_ids[1:] + easy_shells_ids
        # Creating Training Session:
        training_session = TrainingSession(
            user=request.user if request.user.is_authenticated else None,
            shell_count=shell_count,
            last_shell_id=last_shell_id,
            dropped_shell_id=available_ids[0],
        )
        training_session.save()
        training_session.categories.set(category_ids)
        training_session.session_shells.set(available_ids)
        # Saving the session inside user session
        request.session["training_session_id"] = training_session.id
        # TODO: guardar en una variable del User la sesion que tiene activa para acceder a esta despues.
        # Creating the User Shell 
        # TODO: if it already exists update it.
        user_shell = UserShell(user=request.user if request.user.is_authenticated else None, shell_id=available_ids[0])
        user_shell.save()
        return redirect("shells_app:user-shell-detail", pk=user_shell.id)


class ShellInstructionDetailView(DetailView):
    model = UserShell
    template_name = "shell_instruction.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        training_session_id = self.request.session.get("training_session_id")

        if training_session_id:
            try:
                training_session = TrainingSession.objects.get(id=training_session_id)
                completed_shells_count = training_session.completed_shells.count()
                context["current_session_shell"] = completed_shells_count + 1
                context["shell_count"] = training_session.shell_count
            except TrainingSession.DoesNotExist:
                pass
        return context
