from fastapi import FastAPI
import serial
from enum import Enum
from pydantic import BaseModel
from airconditioner_factory import AirConditionerFactory
from switch_factory import SwitchFactory
from cieling_fan import CielFan
from ewelink_interface import Ewelink
from sensibo_interface import SensiboAirConditioner

class ACApi(str, Enum):
    Sensibo = "Sensibo"
    Electra = "Electra"

class SwitchApi(str, Enum):
    Ewelink = "Ewelink"
    Switcher = "Switcher"
    Boiler = "Boiler"

class SwitchRequest(BaseModel):
    power: str

class ACRequest(BaseModel):
    power: str
    fan: str
    mode : str
    temperature : int

class FanRequest(BaseModel):
    light: str = None
    fan: str = None

class ElectraSession:
    def __init__(self):
        self.sid = 0
        self.ts = 0

app = FastAPI()
app.electra_session = ElectraSession()
app.serial = serial.Serial(port='/dev/ttyACM0', baudrate=9600, timeout=1)
app.ewelink = Ewelink()
app.sensibo = SensiboAirConditioner()

@app.get("/acs/{api}/{id}")
async def get_ac_state(api: ACApi, id: str):
    # return {'power': 'OFF', 'temperature': 18, 'fan': "Low", 'mode': "COOL"}
    ac_inst = AirConditionerFactory(api)
    return ac_inst.get_ac_state(id)
    
@app.put("/acs/{api}/{id}")
async def set_ac_state(api: ACApi, id: str, request: ACRequest):
    # pass
    ac_inst = AirConditionerFactory(api)
    ac_inst.set_ac_state(id, request.dict())

@app.get("/switches/{api}/{id}")
async def get_switch_state(api: SwitchApi, id: str):
    # return {'power': 'OFF'}
    switch_inst = SwitchFactory(api)
    return switch_inst.get_switch_state(id)

@app.put("/switches/{api}/{id}")
async def set_switch_state(api: SwitchApi, id: str, request: SwitchRequest):
    # pass
    switch_inst = SwitchFactory(api)
    switch_inst.set_switch_state(id, request.power == 'ON')

@app.put("/fans/{id}")
async def set_fan_state(id: str, request: FanRequest):
    fan = CielFan(id)
    if request.fan is not None:
        fan.set_fan(request.fan)
    if request.light is not None:
        fan.set_light(request.light)