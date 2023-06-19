from django.urls import path

from . import views

app_name = "shells_app"

urlpatterns = [
    path("config", views.CategoriesListView.as_view(), name="config"),
    path("trainer", views.StartTrainingView.as_view(), name="trainer"),
    path('user-shell/<int:pk>/', views.ShellInstructionDetailView.as_view(), name='user-shell-detail'),
    path('user-shell-res/<int:pk>/', views.ShellResolutionDetailView.as_view(), name='user-shell-detail-res'),
    path("next-card/<int:usershell_id>/", views.NextCardView.as_view(), name="next-card"),
    path("trainer-leaderboard/<int:pk>/", views.TrainingSessionDetailView.as_view(), name="trainer-leaderboard"),
]
