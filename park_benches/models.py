# -*- coding: UTF-8 -*-
from __future__ import unicode_literals
import uuid

from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from .base import RandomUniqueIdMixin

@python_2_unicode_compatible
class ParkA(models.Model):
    # uses standard numeric id
    name = models.CharField("Name", max_length=200)

    class Meta:
        verbose_name = "Park (numeric id)"
        verbose_name_plural = "Parks (numeric id)"

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class BenchA(models.Model):
    # uses standard numeric id
    park = models.ForeignKey(ParkA, on_delete=models.CASCADE)
    latitude = models.FloatField("Latitude", help_text="Latitude (Lat.) is the angle between any point and the equator (north pole is at 90; south pole is at -90).", blank=True, null=True)
    longitude = models.FloatField("Longitude", help_text="Longitude (Long.) is the angle east or west of an arbitrary point on Earth from Greenwich (UK), which is the international zero-longitude point (longitude=0 degrees). The anti-meridian of Greenwich is both 180 (direction to east) and -180 (direction to west).", blank=True, null=True)

    class Meta:
        verbose_name = "Bench (numeric id)"
        verbose_name_plural = "Benches (numeric id)"

    def __str__(self):
        return "{latitude}, {longitude}".format(**self.__dict__)


@python_2_unicode_compatible
class ParkB(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  # uses UUID
    name = models.CharField("Name", max_length=200)

    class Meta:
        verbose_name = "Park (uuid)"
        verbose_name_plural = "Parks (uuid)"

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class BenchB(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  # uses UUID
    park = models.ForeignKey(ParkB, on_delete=models.CASCADE)
    latitude = models.FloatField("Latitude", help_text="Latitude (Lat.) is the angle between any point and the equator (north pole is at 90; south pole is at -90).", blank=True, null=True)
    longitude = models.FloatField("Longitude", help_text="Longitude (Long.) is the angle east or west of an arbitrary point on Earth from Greenwich (UK), which is the international zero-longitude point (longitude=0 degrees). The anti-meridian of Greenwich is both 180 (direction to east) and -180 (direction to west).", blank=True, null=True)

    class Meta:
        verbose_name = "Bench (uuid)"
        verbose_name_plural = "Benches (uuid)"

    def __str__(self):
        return "{latitude}, {longitude}".format(**self.__dict__)


@python_2_unicode_compatible
class ParkC(RandomUniqueIdMixin):
    name = models.CharField("Name", max_length=200)

    class Meta:
        verbose_name = "Park (random varchar id)"
        verbose_name_plural = "Parks (random varchar id)"

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class BenchC(RandomUniqueIdMixin):
    park = models.ForeignKey(ParkC, on_delete=models.CASCADE)
    latitude = models.FloatField("Latitude", help_text="Latitude (Lat.) is the angle between any point and the equator (north pole is at 90; south pole is at -90).", blank=True, null=True)
    longitude = models.FloatField("Longitude", help_text="Longitude (Long.) is the angle east or west of an arbitrary point on Earth from Greenwich (UK), which is the international zero-longitude point (longitude=0 degrees). The anti-meridian of Greenwich is both 180 (direction to east) and -180 (direction to west).", blank=True, null=True)

    class Meta:
        verbose_name = "Bench (random varchar id)"
        verbose_name_plural = "Benches (random varchar id)"

    def __str__(self):
        return "{latitude}, {longitude}".format(**self.__dict__)

