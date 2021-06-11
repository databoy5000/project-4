from django.db import models

class Crisis(models.Model):
    SELECT = 1
    TSUNAMI = 2
    CYCLONE = 3
    FLOOD = 4
    EARTHQUAKE = 5
    WAR = 6
    PANDEMIC = 7

    DISASTER_TYPE = [
        (SELECT, 'Select below'),
        (TSUNAMI, 'Tsunami'),
        (CYCLONE, 'Cyclone'),
        (FLOOD, 'Flood'),
        (EARTHQUAKE, 'Eathequake'),
        (WAR, 'War'),
        (PANDEMIC, 'Pandemic'),
    ]


    disaster_type = models.PositiveSmallIntegerField(
        choices=DISASTER_TYPE,
        default=SELECT,
    )
    is_solved = models.BooleanField(null=False)