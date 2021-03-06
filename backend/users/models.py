from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, max_length=254)
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    USERNAME_FIELD = 'email'

    class Meta:
        ordering = ('username', )
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.username
