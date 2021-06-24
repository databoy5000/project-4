from django.db import models
from django.contrib.auth.models import AbstractUser
from rest_framework.exceptions import ValidationError

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
    country = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f'User: {self.username}'

    def get_user_types(self):
        user_types_list = []
        for user_type in self.USER_TYPES:
            user_types_list.append(user_type[1])
        return user_types_list
