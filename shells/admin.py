from django.contrib import admin

from .models import Category, DifficultyLevel, Shell, UserShell, TrainingSession


@admin.register(DifficultyLevel)
class DifficultyAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "value")
    search_fields = ("name", "value")


@admin.register(Shell)
class ShellAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "category", "difficulty_level")
    list_filter = ("category", "difficulty_level")
    search_fields = ("title",)


@admin.register(UserShell)
class UserShellAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "shell", "last_trained_date", "has_liked")
    list_filter = ("user", "shell", "has_liked")
    search_fields = ("user", "shell")


@admin.register(TrainingSession)
class TrainingSessionAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "shell_count", "is_finished")
    list_filter = ("user", "is_finished")
    search_fields = ("user",)


admin.site.register(Category)
