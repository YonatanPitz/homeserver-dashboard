# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from apps.home import views

urlpatterns = [

    # The home page
    path('', views.index, name='home'),
    # Create new routing page
    path('new_routine.html', views.new_routine, name='new_routine'),
    # RPC calls from ajax
    path('get_status', views.get_status, name='get_status'),
    path('set_status', views.set_status, name='set_status'),
    path('get_ids', views.get_ids, name='get_ids'),
    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),

]
