from airconditioner_intf import AirConditionerInterface
from electra import ElectraAPI
from decouple import config
import datetime
import rpc_server

SID_EXPIRATION = datetime.timedelta(hours=1)

class ElectraAirConditioner(AirConditionerInterface):
    def __init__(self):
        super().__init__()
        self.electra_api = self.get_valid_electra_api()
    
    def electra_update_sid(self, sid):
        rpc_server.app.electra_session.sid = sid
        rpc_server.app.electra_session.ts = datetime.datetime.now()

    def electra_validate_token(self, electra_api):
        electra_api.validate_token(config('ELECTRA_IMEI'), config('ELECTRA_TOKEN'))
        self.electra_update_sid(electra_api.sid)

    def electra_set_sid(self, electra_api):
        electra_api.sid = rpc_server.app.electra_session.sid

    def get_device_uid(self, name):
        ac_dict = self.electra_api.get_devices()
        if name not in ac_dict:
            print("AC does not exist in dict")
            return None
        return ac_dict[name]
    
    def get_valid_electra_api(self):
        electra_api = ElectraAPI()
        if rpc_server.app.electra_session.sid == 0:
            print("No SID exists, creating a new one")
            self.electra_validate_token(electra_api)
        else:
            if (datetime.datetime.now() - rpc_server.app.electra_session.ts) > SID_EXPIRATION:
                print("SID expired. creating a new one")
                self.electra_validate_token(electra_api)
            else:
                self.electra_set_sid(electra_api)
        return electra_api

    def get_ac_state(self, name : str) -> dict:
        ac = self.get_device_uid(name)
        resp = {
            'power': 'OFF',
            'temperature': ac.get_temperature(),
            'fan': ac.get_fan_speed().capitalize(),
            'mode': ac.get_mode()
        }
        if ac.is_on():
            resp['power'] = 'ON'
        return resp

    def set_ac_state(self, name : str, state : dict):
        ac = self.get_device_uid(name)
        if state['power'] == 'ON':
            ac.turn_on()
        else:
            ac.turn_off()
        ac.set_mode(state['mode'])
        ac.set_temperature(state['temperature'])
        ac.set_fan_speed(state['fan'].upper())
        self.electra_api.set_state(ac) 