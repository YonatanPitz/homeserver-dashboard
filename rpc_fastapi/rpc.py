from os import stat

from apps.home.models import AC, Switch, Fan
from apps.rpc.airconditioner_factory import AirConditionerFactory
from apps.rpc.switch_factory import SwitchFactory
from apps.rpc.cieling_fan import CielFan



def get_status(entity, id):
    if entity == "switch":
        switch_model = Switch.objects.get(id=id)
        switch_inst = SwitchFactory(switch_model.api)
        return switch_inst.get_switch_state(switch_model.api_id)
    if entity == "AC":
        ac_model = AC.objects.get(id=id)
        ac_inst = AirConditionerFactory(ac_model.api)
        return ac_inst.get_ac_state(ac_model.name)

def set_status(entity, id, status):
    if entity == "switch":
        switch_model = Switch.objects.get(id=id)
        switch_inst = SwitchFactory(switch_model.api)
        switch_inst.set_switch_state(switch_model.api_id, status == 'ON')
    if entity == "AC":
        ac_model = AC.objects.get(id=id)
        ac_inst = AirConditionerFactory(ac_model.api)
        ac_inst.set_ac_state(ac_model.name, status)
    if entity == "fan":
        fan_model = Fan.objects.get(id=id)
        fan = CielFan(fan_model.api_id)
        if "fan" in status:
            fan.set_fan(status['fan'])
        if "light" in status:
            fan.set_light(status['light'])
        