from ewelink_interface import EwelinkInterface
from switcher_interface import Switcher
from boiler_interface import Boiler

def SwitchFactory(api):
    """Factory Method"""
    switch = {
        "Ewelink": EwelinkInterface,
        "Switcher": Switcher,
        "Boiler": Boiler,
    }
    if api in switch:
        return switch[api]()
    else:
        print(f"Unsuspported Switch API {api}")
        return None