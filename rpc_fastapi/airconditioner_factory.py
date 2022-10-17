from electra_interface import ElectraAirConditioner
from sensibo_interface import SensiboInterface

def AirConditionerFactory(api):
    """Factory Method"""
    airconditioner = {
        "Sensibo": SensiboInterface,
        "Electra": ElectraAirConditioner,
    }
 
    return airconditioner[api]()