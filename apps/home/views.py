# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from apps.rpc_server import rpc
from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, HttpResponseBadRequest
from django.template import loader, RequestContext
from django.urls import reverse
import json
import time


@login_required(login_url="/login/")
def index(request):
    context = {'segment': 'index'}

    html_template = loader.get_template('home/index.html')
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
    if is_ajax:
        if request.method == 'GET':
            entity_status = rpc.get_status(entity)
            if entity_status == None:
                return HttpResponseBadRequest('Invalid request')
            else:        
                return JsonResponse({'status': entity_status})
        return JsonResponse({'status': 'Invalid request'}, status=400)
    else:
        return HttpResponseBadRequest('Invalid request')

@login_required(login_url="/login/")
def set_status(request):
    print(request)
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    if is_ajax:
        if request.method == 'PUT':
            data = json.load(request)
            rpc.set_status(data['entity'], data['status'])
            time.sleep(0.5)
            entity_status = rpc.get_status(data['entity'])
            if entity_status == None:
                return HttpResponseBadRequest('Invalid request')
            else:        
                return JsonResponse({'status': entity_status})
        return JsonResponse({'status': 'Invalid request'}, status=400)
    else:
        return HttpResponseBadRequest('Invalid request')