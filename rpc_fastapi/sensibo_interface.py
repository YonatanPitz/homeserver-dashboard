from airconditioner_intf import AirConditionerInterface
from sensibo_client import SensiboClientAPI
from decouple import config
import rpc_server

class SensiboAirConditioner():
    def __init__(self):
        self.client = SensiboClientAPI(config('SENSIBO_KEY'))

class SensiboInterface(AirConditionerInterface):
    def __init__(self):
        super().__init__()
        self.client = rpc_server.app.sensibo.client
    
    def get_ac_state(self, name : str) -> dict:
        devices = self.client.devices()
        uid = devices[name]
        ac_state = self.client.pod_ac_state(uid)
        fan_response_dict = {
            "low":    "Low",
            "medium": "Med",
            "high":   "High",
            "auto":   "Auto"
        }
        resp = {'power': 'OFF', 'temperature': ac_state['targetTemperature'], 'fan': fan_response_dict[ac_state['fanLevel']], 'mode': ac_state['mode'].upper()}
        if ac_state['on']:
            resp['power'] = 'ON' 
        return resp

    def set_ac_state(self, name : str, state : dict):
        devices = self.client.devices()
        uid = devices[name]
        ac_state = self.client.pod_ac_state(uid)
        fan_request_dict = {
            "Low":  "low",
            "Med":  "medium",
            "High": "high",
            "Auto": "auto"
        }
        ac_state['on'] = (state['power'] == 'ON')
        ac_state['mode'] = state['mode'].lower()
        ac_state['targetTemperature'] = state['temperature']
        ac_state['fanLevel'] = fan_request_dict[state['fan']]      
        self.client.pod_change_ac_state(uid, ac_state)
    
    def get_all_ac_states(self) -> dict:
        resp = {}
        devices = self.client.get_all_devices_states()        
        fan_response_dict = {
            "low":    "Low",
            "medium": "Med",
            "high":   "High",
            "auto":   "Auto"
        }
        for name, ac_state in devices.items():
            resp[name] = {'power': 'OFF', 'temperature': ac_state['targetTemperature'], 'fan': fan_response_dict[ac_state['fanLevel']], 'mode': ac_state['mode'].upper()}
            if ac_state['on']:
                resp[name]['power'] = 'ON' 
        return resp