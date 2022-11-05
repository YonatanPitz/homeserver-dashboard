# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib import admin
from .models import AC, Switch, Fan, Routine

# Register your models here.
admin.site.register(AC)
admin.site.register(Switch)
admin.site.register(Fan)
admin.site.register(Routine)