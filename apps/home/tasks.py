import requests
from .models import Switch, AC, Fan, Routine
from django.core.mail import send_mail
from celery import shared_task, group

@shared_task(ignore_result=True)
def celery_set_status(entity, id, status):
    print(entity)
    print(id)
    print(status)
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

@shared_task(ignore_result=True)
def celery_run_routine(id):
    routine = Routine.objects.get(id=id)
    group(celery_set_status.s(action['entity'], action['id'], action['state']) for action in routine.actions)()

@shared_task(ignore_result=True)
def celery_update_all():
    res = requests.get(f'http://127.0.0.1:8001/switches/all').json()
    for switch in Switch.objects.all():
        switch_res = res[switch.api][switch.api_id]
        switch.power = switch_res['power']
        switch.save()
    
    res = requests.get(f'http://127.0.0.1:8001/acs/all').json()
    for ac in AC.objects.all():
        ac_res = res[ac.api][ac.name]
        ac.power = ac_res['power']
        ac.temperature = ac_res['temperature']
        ac.fan = ac_res['fan']
        ac.mode = ac_res['mode']
        ac.save()

@shared_task(ignore_result=True)
def send_email():
    send_mail(
    'Routine Occured',
    'Routine {} occured now.',
    'Homeserver',
    ['pitz.1337@gmail.com'],
    fail_silently=False,
    )
