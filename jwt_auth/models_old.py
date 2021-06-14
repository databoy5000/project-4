# from django.db import models
# from django.contrib.auth.models import AbstractUser

# class User(AbstractUser):
#   is_help_seeker = models.BooleanField('help seeker', default=False)
#   is_NGO = models.BooleanField('NGO', default=False)

# class HelpSeekerUser(models.Model):
#   username = models.CharField(max_length=50)
#   email = models.CharField(max_length=50)
#   profile_image = models.CharField(max_length=250)
#   center_coordinates = models.IntegerField()
#   min_lat = models.IntegerField()
#   max_lat = models.IntegerField()
#   min_long = models.IntegerField()
#   max_long = models.IntegerField()

# class NGOUser(models.Model):
#   username = models.CharField(max_length=50)
#   email = models.CharField(max_length=50)
#   profile_image = models.CharField(max_length=250)