# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib import admin
from .models import AC, Switch

# Register your models here.
admin.site.register(AC)
admin.site.register(Switch)