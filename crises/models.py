from jwt_auth.models import User
from django.db import models

class Resource(models.Model):
    HUMAN = 'Human'
    MATERIAL = 'Material'

    DOCTOR = 'Doctor'
    NURSE = 'Nurse'
    HELPER = 'Helper'
    TEACHER = 'Teacher'
    RESCUER = 'Rescuer'
    MEDICAL = 'Medical'
    NUTRITION = 'Nutrition'
    CLOTHES = 'Clothes'
    SHELTER = 'Shelter'
    TRANSPORT = 'Transport'

    RESOURCE_TYPES = [
        (HUMAN, 'Human'),
        (MATERIAL, 'Material')
    ]

    RESOURCES = [
        (DOCTOR, 'Doctor'),
        (NURSE, 'Nurse'),
        (HELPER, 'Helper'),
        (TEACHER, 'Teacher'),
        (RESCUER, 'Rescuer'),
        (MEDICAL, 'Medical'),
        (NUTRITION, 'Nutrition'),
        (CLOTHES, 'Clothes'),
        (SHELTER, 'Shelter'),
        (TRANSPORT, 'Transport')
    ]

    resource_type = models.CharField(
        max_length=20,
        choices=RESOURCE_TYPES,
    )

    resource_name = models.CharField(
        max_length=20,
        choices=RESOURCES,
        unique=True,
    )

    def __str__(self):
        return f'{self.resource_name} ({self.resource_type})'

class Crisis(models.Model):
    TSUNAMI = 'Tsunami'
    HURRICANE = 'Hurricane'
    FLOOD = 'Flood'
    EARTHQUAKE = 'Earthquake'
    WAR = 'War'
    PANDEMIC = 'Pandemic'
    WILDFIRE = 'Wildfire'

    DISASTER_TYPES = [
        (TSUNAMI, 'Tsunami'),
        (HURRICANE, 'Hurricaine'),
        (FLOOD, 'Flood'),
        (EARTHQUAKE, 'Earthquake'),
        (WAR, 'War'),
        (PANDEMIC, 'Pandemic'),
        (WILDFIRE, 'Wildfire')
    ]

    disaster_type = models.CharField(
        max_length=20,
        choices=DISASTER_TYPES,
    )
    is_solved = models.BooleanField()

    # ! Change 'User' to 'HelpSeekerUser'
    owner = models.ForeignKey(
        'jwt_auth.User',
        related_name = 'crises',
        on_delete = models.CASCADE
    )

    def __str__(self):
        return f'Crisis {self.id} ({self.disaster_type})'

class Request(models.Model):
    LOW = 1
    MEDIUM = 2
    HIGH = 3

    PRIORITY_LEVELS = [
        (LOW, 'Low'),
        (MEDIUM, 'Medium'),
        (HIGH, 'High')
    ]

    quantity = models.PositiveSmallIntegerField()

    crisis = models.ForeignKey(
        Crisis,
        related_name = 'requests',
        on_delete = models.CASCADE
    )

    resource = models.ForeignKey(
        Resource,
        related_name = 'requests',
        on_delete = models.CASCADE
    )

    def __str__(self):
        return f'Request {self.id} on {self.crisis} - {self.quantity} of {self.resource}'

class NGOResource(models.Model):
    quantity = models.PositiveSmallIntegerField()

    ngo_user = models.ForeignKey(
        User,
        related_name = 'ngo_resources',
        on_delete = models.CASCADE
    )

    resource = models.ForeignKey(
        Resource,
        related_name = 'ngo_resources',
        on_delete = models.CASCADE
    )

    def __str__(self):
        return f'{self.quantity} of {self.resource}'