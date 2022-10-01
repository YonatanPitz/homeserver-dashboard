from django.conf import settings
from apps.rpc.sonoff import Sonoff
import pickle
from apps.rpc.switch_intf import SwitchInterface

class Ewelink(SwitchInterface):
    def __init__(self):
        super().__init__()
        try:
            with open("apps/rpc/s_pitz.pkl", "rb") as f:
                self.ewe_client = pickle.load(f)
                self.ewe_client._password = settings.EWELINK_PASSWORD
                self.ewe_client._user_apikey = settings.EWELINK_API_KEY
                self.ewe_client._username = settings.EWELINK_USERNAME
                self.ewe_client.update_devices()
        except:
            self.ewe_client = Sonoff(settings.EWELINK_USERNAME, settings.EWELINK_PASSWORD, "as")
            with open("apps/rpc/s_pitz.pkl", "wb") as f:
                self.ewe_client._password = ""
                self.ewe_client._user_apikey = ""
                self.ewe_client._username = ""
                pickle.dump(self.ewe_client, f)
            self.ewe_client._password = settings.EWELINK_PASSWORD
            self.ewe_client._user_apikey = settings.EWELINK_API_KEY
            self.ewe_client._username = settings.EWELINK_USERNAME
                
    def get_switch_state(self, id : str) -> bool:
        device = self.ewe_client.get_device(id)
        return {'power': device['params']['switch'].upper()}

    def set_switch_state(self, id : str, state : bool):
        self.ewe_client.switch(state, id, None)