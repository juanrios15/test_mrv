import os

from django.db import models

from users.models import MrvUser


class Category(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class DifficultyLevel(models.Model):
    name = models.CharField(max_length=50)
    value = models.IntegerField()

    class Meta:
        verbose_name = "Difficulty Level"
        verbose_name_plural = "Difficulty Levels"

    def __str__(self):
        return self.name


def instruction_file_path(instance, filename):
    return os.path.join("images/instructions", filename)


def resolution_file_path(instance, filename):
    return os.path.join("images/resolutions", filename)


class Shell(models.Model):
    title = models.CharField(max_length=250)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    difficulty_level = models.ForeignKey(DifficultyLevel, on_delete=models.CASCADE)
    instruction_text = models.CharField(max_length=500, blank=True, null=True)
    instruction_image = models.ImageField(upload_to=instruction_file_path)
    resolution_text = models.CharField(max_length=500, blank=True, null=True)
    resolution_image = models.ImageField(upload_to=resolution_file_path)

    class Meta:
        verbose_name = "Shell"
        verbose_name_plural = "Shells"

    def __str__(self):
        return self.title


class UserShell(models.Model):
    user = models.ForeignKey(MrvUser, on_delete=models.CASCADE)
    shell = models.ForeignKey(Shell, on_delete=models.CASCADE)
    last_trained_date = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True)
    time_spent_drill_instruction = models.FloatField(null=True, blank=True)
    time_spent_drill_resolution = models.FloatField(null=True, blank=True)
    trained_count = models.IntegerField(null=True, blank=True)
    difficulty_evaluation = models.BooleanField(default=False)  # TODO: It could have what evaluation the user gave
    has_liked = models.BooleanField(default=False)
    created_time = models.DateField(auto_now=False, auto_now_add=True)
    updated_time = models.DateField(auto_now=True)

    class Meta:
        verbose_name = "User Shell"
        verbose_name_plural = "User Shells"

    def __str__(self):
        return self.shell.title


class TrainingSession(models.Model):
    user = models.ForeignKey(MrvUser, on_delete=models.CASCADE)
    shell_count = models.IntegerField(default=0)  # TODO: What is this counting?
    categories = models.ManyToManyField(Category, blank=True)
    candidate_shells = models.ManyToManyField("Shell", related_name="candidate_shells", blank=True)
    session_shells = models.ManyToManyField("Shell", related_name="session_shells", blank=True)
    last_shell = models.ForeignKey("Shell", on_delete=models.CASCADE, related_name="last_shell", blank=True)
    dropped_shell = models.ForeignKey(
        "Shell", on_delete=models.CASCADE, related_name="dropped_shell", blank=True
    )  # TODO: Ask which one is this?
    completed_shells = models.ManyToManyField("Shell", related_name="completed_shells", blank=True)
    is_finished = models.BooleanField(default=False)
    created_time = models.DateField(auto_now=False, auto_now_add=True)
    updated_time = models.DateField(auto_now=True)
    # TODO: It could have started_time and finished_time.

    class Meta:
        verbose_name = "Training session"
        verbose_name_plural = "Training sessions"

    def __str__(self):
        return self.shell
