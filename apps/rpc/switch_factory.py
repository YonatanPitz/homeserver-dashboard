from apps.rpc.ewelink_interface import Ewelink

def SwitchFactory(api):
    """Factory Method"""
    switch = {
        "Ewelink": Ewelink,
    }
    if api in switch:
        return switch[api]()
    else:
        print(f"Unsuspported Switch API {api}")
        return None