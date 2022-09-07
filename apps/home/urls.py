# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from apps.home import views

urlpatterns = [

    # The home page
    path('', views.index, name='home'),
    # RPC calls from ajax
    path('get_status', views.get_status, name='get_status'),
    path('set_status', views.set_status, name='set_status'),
    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),

]
