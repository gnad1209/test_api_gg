from django.db import models
from django.utils import timezone

# Create your models here.
class Product(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length = 255, unique = True)
    describe = models.CharField(max_length = 255)
    time_created = models.DateTimeField(default = timezone.datetime.now())

    def __str__(self):
        return self.name