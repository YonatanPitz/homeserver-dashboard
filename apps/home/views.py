# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from os import stat
from apps.rpc import rpc
from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, HttpResponseBadRequest
from django.template import loader, RequestContext
from django.urls import reverse
import json
import time
from .models import AC, Switch


@login_required(login_url="/login/")
def index(request):
    context = {'segment': 'index'}
    html_template = loader.get_template('home/index.html')
    context['acs_list'] = [{'id': x.id, 'name': x.name, 'api': x.api, 'templist': [i for i in range(17,31)]} for x in AC.objects.all()]
    context['switches_list'] = [{'id': x.id, 'name': x.name, 'api': x.api} for x in Switch.objects.all()]
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def get_status(request):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    entity = request.GET.get('entity', '')
    id = request.GET.get('id', 0)
    if is_ajax:
        if request.method == 'GET':
            entity_status = rpc.get_status(entity, id)
            if entity_status == None:
                return HttpResponseBadRequest('Invalid request')
            else:        
                return JsonResponse(entity_status)
        return JsonResponse({'status': 'Invalid request'}, status=400)
    else:
        return HttpResponseBadRequest('Invalid request')

@login_required(login_url="/login/")
def set_status(request):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    if is_ajax:
        if request.method == 'PUT':
            data = json.load(request)
            rpc.set_status(data['entity'], data['id'], data['status'])
            time.sleep(0.5)
            return JsonResponse({'rpc_status': 'OK'})
    else:
        return HttpResponseBadRequest('Invalid request')

@login_required(login_url="/login/")
def get_ids(request):
    if request.method == 'GET':
        entity = request.GET.get('entity', 0)
        if entity == 'AC':
            return JsonResponse({'ac_ids': [x.id for x in AC.objects.all()]})
        elif entity == 'switch':
            return JsonResponse({'switch_ids': [x.id for x in Switch.objects.all()]})
        else:
            return HttpResponseBadRequest('Invalid request')
    else:
        return HttpResponseBadRequest('Invalid request')