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
    class POWER_ENUM(models.TextChoices):
        ON = "ON"
        OFF = "OFF"
    power = models.CharField(max_length=5, choices=POWER_ENUM.choices, default=POWER_ENUM.OFF)
    class FAN_ENUM(models.TextChoices):
        AUTO = "Auto"
        LOW = "Low"
        MED = "Med"
        HIGH = "High"
    fan = models.CharField(max_length=5, choices=FAN_ENUM.choices, default=FAN_ENUM.LOW)
    class MODE_ENUM(models.TextChoices):
        HEAT = "HEAT"
        COOL = "COOL"
        FAN = "FAN"
    mode = models.CharField(max_length=5, choices=MODE_ENUM.choices, default=MODE_ENUM.COOL)
    temperature = models.IntegerField(default=18)

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
    class POWER_ENUM(models.TextChoices):
        ON = "ON"
        OFF = "OFF"
    power = models.CharField(max_length=5, choices=POWER_ENUM.choices, default=POWER_ENUM.OFF)

class Fan(models.Model):
    def __str__(self):
        return self.name

    name = models.CharField(max_length=200)
    api_id = models.CharField(max_length=200)

class Routine(models.Model):
    def __str__(self):
        return self.name
    
    name = models.CharField(max_length=200)
    actions = models.JSONField(default=[])

# class Action(models.Model):
#     class ENTITY_TYPE(models.TextChoices):
#         SWITCH = 'Switch'
#         AC = 'AC'
#         FAN = 'Fan'

#     entity_type = models.CharField(
#         max_length=10,
#         choices=ENTITY_TYPE.choices,
#         default=ENTITY_TYPE.SWITCH,
#     )

#     api_id = models.CharField(max_length=200)
#     # state = models.JSONField(default=[])
    
#     def __str__(self):
#     	return f"{self.entity_type}: {self.api_id}"