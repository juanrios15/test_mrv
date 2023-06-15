from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.shortcuts import render


class LoginMrvView(LoginView):
    template_name = "login.html"
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy("home")
