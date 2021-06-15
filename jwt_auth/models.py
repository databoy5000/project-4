from django.db import models
from django.contrib.auth.models import AbstractUser

# class User(AbstractUser):
#   is_help_seeker = models.BooleanField('help seeker', default=False)
#   is_NGO = models.BooleanField('NGO', default=False)

class User(AbstractUser):
    username = models.CharField(max_length=50, unique=True)
    email = models.CharField(max_length=50, unique=True)
    profile_picture_url = models.CharField(max_length=250)
    country = models.CharField(max_length=50)