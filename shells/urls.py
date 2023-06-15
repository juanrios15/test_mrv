from django.urls import path

from . import views

app_name = "shells_app"

urlpatterns = [
    path("config", views.CategoriesListView.as_view(), name="config"),
    path("trainer", views.StartTrainingView.as_view(), name="trainer"),
]
