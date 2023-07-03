from django.contrib import admin
from django.urls import path

from . import views

app_name = "users_app"

urlpatterns = [
    path("login", views.LoginMrvView.as_view(), name="login"),
    path('logout', views.LogoutMrvView.as_view(), name="logout"),
    path('register', views.RegisterMrvView.as_view(), name="register"),
]
