# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import template
from django.contrib.auth.decorators import login_required
from django.forms import formset_factory
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, HttpResponseBadRequest
from django.template import loader
from django.urls import reverse
import json
import time
import requests
from .models import AC, Switch, Fan, Routine

@login_required(login_url="/login/")
def index(request):
    context = {'segment': 'index'}
    html_template = loader.get_template('home/index.html')
    context['acs_list'] = [{'id': x.id, 'name': x.name, 'api': x.api, 'templist': [i for i in range(17,31)]} for x in AC.objects.all()]
    icon_dict = {
        'Bulb': "ni ni-bulb-61",
        'Coffee': "fa fa-mug-hot",
        'Shower': "fa fa-shower",
    }
    context['switches_list'] = [{'id': x.id, 'name': x.name, 'api': x.api, 'icon': icon_dict[x.icon]} for x in Switch.objects.all()]
    context['fans_list'] = [{'id': x.id, 'name': x.name} for x in Fan.objects.all()]
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def new_routine(request):
    if request.method == 'POST':
        print(request.POST['RoutineName'])
        print(request.POST['NumOfActions'])
    # else:
        # form = RoutineForm()
        # formset = formset_factory(ActionForm)
        # formset = ActionFormSet(queryset=Action.objects.none())
        # pass
    context = {'segment': 'new_routine'}
    html_template = loader.get_template('home/new_routine.html')
    context['acs_list'] = [{'id': x.id, 'name': x.name} for x in AC.objects.all()]
    context['switches_list'] = [{'id': x.id, 'name': x.name} for x in Switch.objects.all()]
    context['fans_list'] = [{'id': x.id, 'name': x.name} for x in Fan.objects.all()]
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def routines(request):
    if request.method == 'GET':
        context = {'segment': 'routines'}
        html_template = loader.get_template('home/routines.html')
        context['routines'] = []
        for routine in Routine.objects.all():
            routine_dict = {'id': routine.id, 'name': routine.name, 'actions': []}
            for action in routine.actions:
                action_dict = {'state': action['state']}
                if action['entity'] == 'switch':
                    action_dict['entity_name'] = Switch.objects.get(id=action['id']).name
                if action['entity'] == 'AC':
                    action_dict['entity_name'] = AC.objects.get(id=action['id']).name
                if action['entity'] == 'fan':
                    action_dict['entity_name'] = Fan.objects.get(id=action['id']).name
                routine_dict['actions'].append(action_dict)
            context['routines'].append(routine_dict)
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
            entity_status = None
            # entity_status = client.call_rpc('get_status', entity, id)
            # entity_status = {'Test': 'Test'}
            if entity == 'AC':
                ac_model = AC.objects.get(id=id)
                entity_status = requests.get(f'http://127.0.0.1:8001/acs/{ac_model.api}/{ac_model.name}').json()
            if entity == 'switch':
                switch_model = Switch.objects.get(id=id)
                entity_status = requests.get(f'http://127.0.0.1:8001/switches/{switch_model.api}/{switch_model.api_id}').json()
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
            entity = data['entity']
            id = data['id']
            status = data['status']
            headers = {'content-type' : 'application/json'}
            if entity == 'AC':
                ac_model = AC.objects.get(id=id)
                requests.put(f'http://127.0.0.1:8001/acs/{ac_model.api}/{ac_model.name}', json=status, headers=headers)
            if entity == 'switch':
                switch_model = Switch.objects.get(id=id)
                requests.put(f'http://127.0.0.1:8001/switches/{switch_model.api}/{switch_model.api_id}', json=status, headers=headers)
            if entity == 'fan':
                fan_model = Fan.objects.get(id=id)
                requests.put(f'http://127.0.0.1:8001/fans/{fan_model.api_id}', json=status, headers=headers)
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