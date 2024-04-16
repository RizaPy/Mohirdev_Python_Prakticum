from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):
    username = models.CharField(max_length=50)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=100, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    image = models.ImageField(upload_to='users/', null=True, blank=True)

    def __str__(self):
        return self.username

