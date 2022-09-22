from apps.rpc.electra_interface import ElectraAirConditioner
from apps.rpc.sensibo_interface import SensiboAirConditioner

def AirConditionerFactory(api):
    """Factory Method"""
    airconditioner = {
        "Sensibo": SensiboAirConditioner,
        "Electra": ElectraAirConditioner,
    }
 
    return airconditioner[api]()