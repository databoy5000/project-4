from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    username = models.CharField(max_length=50, unique=True)
    email = models.CharField(max_length=50, unique=True)
    profile_picture_url = models.CharField(max_length=250)
    country = models.CharField(max_length=50)
