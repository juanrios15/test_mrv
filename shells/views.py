import math
from datetime import datetime, date

from django.http import HttpResponseNotFound, HttpResponse
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
        user_shell = UserShell(user=request.user if request.user.is_authenticated else None, shell_id=available_ids[0])
        user_shell.save()
        return redirect("shells_app:user-shell-detail", pk=user_shell.id)


class ShellDetailView(DetailView):
    model = UserShell

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


class ShellInstructionDetailView(ShellDetailView):
    template_name = "shell_instruction.html"

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.opened_resolution_time is not None:
            self.object.time_spent_drill_resolution += (
                datetime.now().astimezone() - self.object.opened_resolution_time
            ).total_seconds()
            self.object.opened_resolution_time = None
            self.object.save()

        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)


class ShellResolutionDetailView(ShellDetailView):
    template_name = "shell_resolution.html"

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.opened_resolution_time is not None:
            self.object.time_spent_drill_resolution += (
                datetime.now().astimezone() - self.object.opened_resolution_time
            ).total_seconds()
        self.object.opened_resolution_time = datetime.now().astimezone()
        self.object.time_spent_drill_instruction = (
            datetime.now().astimezone() - self.object.created_time
        ).total_seconds() - self.object.time_spent_drill_resolution
        self.object.save()
        context = self.get_context_data(object=self.object)
        context["is_last_shell"] = False
        training_session_id = self.request.session.get("training_session_id")
        if training_session_id:
            try:
                training_session = TrainingSession.objects.get(id=training_session_id)
                if self.object.shell.id == training_session.last_shell.id:
                    context["is_last_shell"] = True
            except TrainingSession.DoesNotExist:
                pass
        return self.render_to_response(context)


class NextCardView(View):
    def get(self, request, usershell_id, *args, **kwargs):
        user_shell = UserShell.objects.get(id=usershell_id)
        user_shell.time_spent_drill_resolution += (
            datetime.now().astimezone() - user_shell.opened_resolution_time
        ).total_seconds()
        user_shell.last_trained_date = date.today()
        user_shell.save()
        training_session_id = self.request.session.get("training_session_id")
        if training_session_id:
            try:
                training_session = TrainingSession.objects.get(id=training_session_id)
                completed_shells = training_session.completed_shells.all()
                training_session.completed_shells.add(user_shell.shell)
                new_shell = training_session.session_shells.exclude(id__in=completed_shells).first()
                training_session.dropped_shell = new_shell
                training_session.save()

                # Selecting next card
                if not new_shell:
                    if training_session.last_shell not in completed_shells:
                        new_shell = training_session.last_shell
                    else:
                        training_session.is_finished = True
                        training_session.completed_shells.add(user_shell.shell)
                        training_session.time_spent_session = (
                            datetime.now().astimezone() - training_session.created_time
                        ).total_seconds()
                        training_session.save()
                        return redirect("shells_app:trainer-leaderboard", pk=training_session.id)
                user_shell = UserShell(
                    user=request.user if request.user.is_authenticated else None, shell_id=new_shell.id
                )
                user_shell.save()
                return redirect("shells_app:user-shell-detail", pk=user_shell.id)

            except TrainingSession.DoesNotExist:
                pass
        return HttpResponseNotFound("Training session not found.")


class TrainingSessionDetailView(DetailView):
    model = TrainingSession
    template_name = "trainer_leaderboard.html"

    def seconds_to_min_sec(self, seconds):
        minutes = int(seconds // 60)
        seconds = int(seconds % 60)
        print("sec", seconds)
        return f"{minutes}m {seconds}s"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            user_shell_count = UserShell.objects.filter(user=self.request.user).values('shell').distinct().count()
            total_shell_count = Shell.objects.count()
            context['card_count'] = total_shell_count - user_shell_count
        else:
            total_shell_count = Shell.objects.count()
            context['card_count'] = total_shell_count - self.object.shell_count
        if context['object'].time_spent_session is not None:
            context['time_spent_session_str'] = self.seconds_to_min_sec(context['object'].time_spent_session)

        return context

class UserShellLikedView(View):
    def get(self, request, *args, **kwargs):
        user_shell_id = kwargs["pk"]
        user_shell = UserShell.objects.get(id=user_shell_id)
        user_shell.has_liked = True
        user_shell.save()

        message = "Liked!"
        return HttpResponse(message)


class UserShellEasyReviewView(View):
    def get(self, request, *args, **kwargs):
        EASY_REVIEW = 1
        user_shell_id = kwargs["pk"]
        user_shell = UserShell.objects.get(id=user_shell_id)

        user_shell.difficulty_evaluation_id = EASY_REVIEW
        user_shell.save()

        message = "Reviewed!"
        return HttpResponse(message)


class UserShellHardReviewView(View):
    def get(self, request, *args, **kwargs):
        HARD_REVIEW = 3
        user_shell_id = kwargs["pk"]
        user_shell = UserShell.objects.get(id=user_shell_id)

        user_shell.difficulty_evaluation_id = HARD_REVIEW
        user_shell.save()

        message = "Reviewed!"
        return HttpResponse(message)
