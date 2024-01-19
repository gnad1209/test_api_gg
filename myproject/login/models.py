# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from rest_framework.permissions import BasePermission


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username


class BlacklistedToken(models.Model): 
    token = models.CharField(max_length=255, unique=True)
    user = models.ForeignKey(CustomUser, related_name="token_user", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.token
