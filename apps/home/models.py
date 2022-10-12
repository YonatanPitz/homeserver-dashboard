# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class AC(models.Model):
    def __str__(self):
        return self.name

    name = models.CharField(max_length=200)
    class AC_API(models.TextChoices):
        SENSIBO = 'Sensibo'
        ELECTRA = 'Electra'

    api = models.CharField(
        max_length=10,
        choices=AC_API.choices,
        default=AC_API.SENSIBO,
    )

class Switch(models.Model):
    def __str__(self):
        return self.name

    name = models.CharField(max_length=200)
    api_id   = models.CharField(max_length=200)
    class SWITCH_API(models.TextChoices):
        EWELINK = 'Ewelink'
        SWITCHER = 'Switcher'
        BOILER = 'Boiler'
    api = models.CharField(
        max_length=10,
        choices=SWITCH_API.choices,
        default=SWITCH_API.EWELINK,
    )

    class SWITCH_ICON(models.TextChoices):
        BULB = 'Bulb'
        COFFEE = 'Coffee'
        SHOWER = 'Shower'

    icon = models.CharField(
        max_length=10,
        choices=SWITCH_ICON.choices,
        default=SWITCH_ICON.BULB,
    )

class Fan(models.Model):
    def __str__(self):
        return self.name

    name = models.CharField(max_length=200)
    api_id = models.CharField(max_length=200)