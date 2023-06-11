from django.db import models
from django.contrib.auth.models import AbstractUser


class MrvUser(AbstractUser):
    is_logged_in = models.BooleanField(default=False)
    # TODO: Ask about ZONE field
