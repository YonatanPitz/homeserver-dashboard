from decouple import config
from sonoff import Sonoff
import pickle
from switch_intf import SwitchInterface
import rpc_server

class EwelinkInterface(SwitchInterface):
    def __init__(self):
        super().__init__()
                
    def get_switch_state(self, id : str):
        device = rpc_server.app.ewelink.ewe_client.get_device(id)
        return {'power': device['params']['switch'].upper()}

    def set_switch_state(self, id : str, state : bool):
        rpc_server.app.ewelink.ewe_client.switch(state, id, None)

    def get_all_switch_states(self) -> dict:
        devices = rpc_server.app.ewelink.ewe_client.get_devices(force_update=True)
        return {x['deviceid']: {'power': x['params']['switch'].upper()} for x in devices}
        # return devices

class Ewelink():
    def __init__(self):
        try:
            with open("s_pitz.pkl", "rb") as f:
                self.ewe_client = pickle.load(f)
                self.ewe_client._password = config('EWELINK_PASSWORD')
                self.ewe_client._user_apikey = config('EWELINK_API_KEY')
                self.ewe_client._username = config('EWELINK_USERNAME')
                self.ewe_client.update_devices()
        except:
            self.ewe_client = Sonoff(config('EWELINK_USERNAME'), config('EWELINK_PASSWORD'), "as")
            with open("s_pitz.pkl", "wb") as f:
                self.ewe_client._password = ""
                self.ewe_client._user_apikey = ""
                self.ewe_client._username = ""
                pickle.dump(self.ewe_client, f)
            self.ewe_client._password = config('EWELINK_PASSWORD')
            self.ewe_client._user_apikey = config('EWELINK_API_KEY')
            self.ewe_client._username = config('EWELINK_USERNAME')