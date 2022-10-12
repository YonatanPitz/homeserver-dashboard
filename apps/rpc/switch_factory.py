from apps.rpc.ewelink_interface import Ewelink
from apps.rpc.switcher_interface import Switcher
from apps.rpc.boiler_interface import Boiler

def SwitchFactory(api):
    """Factory Method"""
    switch = {
        "Ewelink": Ewelink,
        "Switcher": Switcher,
        "Boiler": Boiler,
    }
    if api in switch:
        return switch[api]()
    else:
        print(f"Unsuspported Switch API {api}")
        return None