from django.db import models
from django.contrib.auth.models import User

class Reservable(models.Model):
    name = models.CharField(max_length=255)
    capacity = models.IntegerField(default=1)
    location = models.CharField(max_length=100, default="")
    description = models.TextField(default="")
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
