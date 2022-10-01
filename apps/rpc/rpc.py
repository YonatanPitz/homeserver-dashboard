from os import stat

from apps.rpc import boiler
from apps.home.models import AC, Switch
from apps.rpc.airconditioner_factory import AirConditionerFactory
from apps.rpc.switch_factory import SwitchFactory

def get_status_boiler():
    boil = boiler.BoilerInterface()
    return {'power': boil.get_state().value}

def get_status(entity, id):
    if entity == "boiler":
        return get_status_boiler()
    if entity == "switch":
        switch_model = Switch.objects.get(id=id)
        switch_inst = SwitchFactory(switch_model.api)
        return switch_inst.get_switch_state(switch_model.api_id)
    if entity == "AC":
        ac_model = AC.objects.get(id=id)
        ac_inst = AirConditionerFactory(ac_model.api)
        return ac_inst.get_ac_state(ac_model.name)

def set_status(entity, id, status):
    if entity == "boiler":
        boil = boiler.BoilerInterface()
        if status == 'ON':
            boil.turn_on()
        if status == 'OFF':
            boil.turn_off()
    if entity == "switch":
        switch_model = Switch.objects.get(id=id)
        switch_inst = SwitchFactory(switch_model.api)
        switch_inst.set_switch_state(switch_model.api_id, status == 'ON')
    if entity == "AC":
        ac_model = AC.objects.get(id=id)
        ac_inst = AirConditionerFactory(ac_model.api)
        ac_inst.set_ac_state(ac_model.name, status)