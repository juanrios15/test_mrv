from django.db import models
from django.contrib.auth.models import AbstractUser


class MrvUser(AbstractUser):
    email = models.EmailField(unique=True)
    is_logged_in = models.BooleanField(default=False)
    # TODO: Ask about ZONE field

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []
