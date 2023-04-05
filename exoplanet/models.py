from django.contrib.auth.models import User
from django.db import models


class Exoplanet(models.Model):
    HABITABILITY_CHOICES = (
        ('NH', 'Non Habitable'),
        ('OH', 'Optimistically Habitable'),
        ('CH', 'Conservatively Habitable'),
    )

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    planet_name = models.CharField(max_length=255)
    star_name = models.CharField(max_length=255, null=True, blank=True)
    habitability = models.CharField(max_length=2, choices=HABITABILITY_CHOICES)
    planet_radius = models.FloatField(null=True, blank=True)
    planet_period = models.FloatField(null=True, blank=True)
    planet_temperature_equilibrium = models.FloatField(null=True, blank=True)
    planet_temperature_equilibrium_min = models.FloatField(null=True, blank=True)
    planet_temperature_equilibrium_max = models.FloatField(null=True, blank=True)
    distance_to_star = models.FloatField(null=True, blank=True)
    star_mass = models.FloatField(null=True, blank=True)
    star_radius = models.FloatField(null=True, blank=True)
    star_temperature = models.FloatField(null=True, blank=True)
    star_luminosity = models.FloatField(null=True, blank=True)
    star_metallicity = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.planet_name