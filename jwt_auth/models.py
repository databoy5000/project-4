from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    HELPSEEKER = 'Help-seeker'
    NGO = "NGO"

    USER_TYPES = [
      (HELPSEEKER, 'Help-seeker'),
      (NGO, 'NGO')
    ]

    user_type = models.CharField(
      max_length=20,
      choices=USER_TYPES,
    )
    username = models.CharField(max_length=50, unique=True)
    email = models.CharField(max_length=50, unique=True)
    profile_picture_url = models.CharField(max_length=250)
    country = models.CharField(max_length=50, unique=True, null=True)

    def __str__(self):
        return f'User: {self.username}'
