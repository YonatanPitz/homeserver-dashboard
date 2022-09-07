from apps.rpc_server import boiler

def get_status(entity):
    if entity == "boiler":
        boil = boiler.BoilerInterface()
        return boil.get_state().value
    else:
        return None

def set_status(entity, status):
    if entity == "boiler":
        boil = boiler.BoilerInterface()
        if status == 'on':
            boil.turn_on()
        if status == 'off':
            boil.turn_off()