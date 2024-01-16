# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    
    # Add custom fields here, if needed

    def __str__(self):
        return self.username
    
class Product(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length = 255, unique = True)
    describe = models.CharField(max_length = 255)
    time_created = models.DateTimeField(default = timezone.datetime.now())

    def __str__(self):
        return self.name


class BlacklistedToken(models.Model):
    token = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.token