from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.shortcuts import render


class LoginMrvView(LoginView):
    template_name = "login.html"
    redirect_authenticated_user = True
    success_url = reverse_lazy("profile")
