from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager


class MrvUserManager(UserManager):
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_logged_in', False)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email=email, username=email, password=password, **extra_fields)


class MrvUser(AbstractUser):
    email = models.EmailField(unique=True)
    is_logged_in = models.BooleanField(default=False)
    # TODO: Ask about ZONE field

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = MrvUserManager()

