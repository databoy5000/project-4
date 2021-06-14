from django.apps import AppConfig
from django.db import models
from django.contrib.auth.models import AbstractUser

class JwtAuthConfig(AppConfig):
  default_auto_field = 'django.db.models.BigAutoField'
  name = 'jwt_auth'
  