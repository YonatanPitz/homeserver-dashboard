from distutils.sysconfig import get_config_var
import requests
import json
from dataclasses import dataclass
from typing import Dict, List
    
MAX_TEMP = 30
MIN_TEMP = 17


@dataclass
class OperationMode:
    MODE_COOL = "COOL"
    MODE_HEAT = "HEAT"
    MODE_AUTO = "AUTO"
    MODE_DRY = "DRY"
    MODE_FAN = "FAN"
    FAN_SPEED_LOW = "LOW"
    FAN_SPEED_MED = "MED"
    FAN_SPEED_HIGH = "HIGH"
    FAN_SPEED_AUTO = "AUTO"
    ON = "ON"
    OFF = "OFF"
    STANDBY = "STBY"


@dataclass
class Feature:
    V_SWING = 0
    H_SWING = 1


def generate_imei():
    from math import floor, pow
    from random import randint
    minimum = int(pow(10, 7))
    maximum = int(pow(10, 8) - 1)
    return f"2b950000{str(floor(randint(minimum, maximum)))}"

class ElectraAPI(object):
    def __init__(self):
        self.url = "https://app.ecpiot.co.il/mobile/mobilecommand"

    def send_request(self, payload):
        return requests.post(self.url, json=payload, headers={"user-agent": "Electra Client"})
    
    def send_otp(self, imei, phone_number):
        payload = {
            "pvdid": 1,
            "id": 99,
            "cmd": "SEND_OTP",
            "data": {"imei": imei, "phone": phone_number},
        }
        return self.send_request(payload)


    def check_otp(self, imei, phone_number, otp):
        payload = {
                    "pvdid": 1,
                    "id": 99,
                    "cmd": "CHECK_OTP",
                    "data": {
                        "imei": imei,
                        "phone": phone_number,
                        "code": otp,
                        "os": "android",
                        "osver": "M4B30Z",
                    },
                }
        return self.send_request(payload)

    def validate_token(self, imei, token):
        payload = {
                    "pvdid": 1,
                    "id": 99,
                    "cmd": "VALIDATE_TOKEN",
                    "data": {
                        "imei": imei,
                        "token": token,
                        "os": "android",
                        "osver": "M4B30Z",
                },
            }
        resp = self.send_request(payload)
        self.sid = json.loads(resp.text)['data']['sid']
        return self.sid

    def get_devices(self):
        payload = {"pvdid": 1, "id": 99, "cmd": "GET_DEVICES", "sid": self.sid}
        resp = self.send_request(payload)
        if resp.status_code != 200:
            print(f"Error getting devices {resp}")

        get_devices_resp = json.loads(resp.text)
    
        ac_dict = {}

        for ac in get_devices_resp['data']['devices']:
            if ac["deviceTypeName"] == "A/C":
                print(f"A/C {ac['name']} - ID {ac['id']}")
                electra_ac: ElectraAirConditioner = ElectraAirConditioner(ac)
                self.get_last_telemtry(electra_ac)
                electra_ac.update_features()
                ac_dict[electra_ac.name] = electra_ac
        return ac_dict
    
    def set_state(self, ac):
        json_command = ac.get_operation_state()
        payload = {
            "pvdid": 1,
            "id": 99,
            "cmd": "SEND_COMMAND",
            "sid": self.sid,
            "data": {"id": ac.id, "commandJson": json_command},
        }
        return self.send_request(payload)
    
    def get_last_telemtry(self, ac):
        payload = {
            "pvdid": 1,
            "id": 99,
            "cmd": "GET_LAST_TELEMETRY",
            "sid": self.sid,
            "data": {"id": ac.id, "commandName": "OPER,DIAG_L2"},
        }

        resp = self.send_request(payload)
        if resp.status_code != 200:
            print(f"Failed to get AC operation state: {resp}")
        else:
            ac.update_operation_states(json.loads(resp.text)["data"])


class ElectraAirConditioner(object):
    def __init__(self, data) -> None:
        self.id: str = data["id"]
        self.name: str = data["name"]
        self.regdate: str = data["regdate"]
        self.model = data["model"]
        self.mac: str = data["mac"]
        self.serial_number: str = data["sn"]
        self.manufactor: str = data["manufactor"]
        self.type: str = data["deviceTypeName"]
        self.status: str = data["status"]
        self.token: str = data["deviceToken"]
        self._time_delta: int = 0
        self.features: List[Feature] = []
        self.current_mode: str = None
        self.collected_measure: int = None
        self._oper_data: Dict = None

    def is_disconnected(self, thresh_sec: int = 60) -> bool:
        return self._time_delta > thresh_sec

    def update_features(self) -> None:
        if "VSWING" in self._oper_data:
            self.features.append(Feature.V_SWING)
        if "HSWING" in self._oper_data:
            self.features.append(Feature.H_SWING)

    def get_sensor_temperature(self) -> int:
        return self.collected_measure

    def get_mode(self) -> str:
        return self._oper_data["AC_MODE"]

    def set_mode(self, mode: str) -> None:
        if mode in [
            OperationMode.MODE_AUTO,
            OperationMode.MODE_COOL,
            OperationMode.MODE_DRY,
            OperationMode.MODE_FAN,
            OperationMode.MODE_HEAT,
        ]:
            if mode != self._oper_data["AC_MODE"]:
                self._oper_data["AC_MODE"] = mode

    def set_horizontal_swing(self, enable: bool):
        if "HSWING" in self._oper_data:
            self._oper_data["HSWING"] = (
                OperationMode.ON if enable else OperationMode.OFF
            )

    def set_vertical_swing(self, enable: bool):
        if "VSWING" in self._oper_data:
            self._oper_data["VSWING"] = (
                OperationMode.ON if enable else OperationMode.OFF
            )

    def is_vertical_swing(self):
        if "VSWING" in self._oper_data:
            return self._oper_data["VSWING"] == OperationMode.ON
        return False

    def is_horizontal_swing(self):
        if "HSWING" in self._oper_data:
            return self._oper_data["HSWING"] == OperationMode.ON
        return False

    def is_on(self):
        if "TURN_ON_OFF" in self._oper_data:
            return self._oper_data["TURN_ON_OFF"] == OperationMode.ON
        else:
            return self._oper_data["AC_MODE"] != OperationMode.STANDBY

    def turn_on(self):
        if not self.is_on():
            if "TURN_ON_OFF" in self._oper_data:
                self._oper_data["TURN_ON_OFF"] = OperationMode.ON

    def turn_off(self):
        if self.is_on():
            if "TURN_ON_OFF" in self._oper_data:
                self._oper_data["TURN_ON_OFF"] = OperationMode.OFF
            else:
                self._oper_data["AC_MODE"] = OperationMode.STANDBY

    def get_temperature(self):
        return int(self._oper_data["SPT"])

    def set_temperature(self, val: int):
        if self.get_temperature() != val:
            self._oper_data["SPT"] = str(val)

    def get_fan_speed(self):
        return self._oper_data["FANSPD"]

    def set_fan_speed(self, speed):
        if speed in [
            OperationMode.FAN_SPEED_AUTO,
            OperationMode.FAN_SPEED_HIGH,
            OperationMode.FAN_SPEED_MED,
            OperationMode.FAN_SPEED_LOW,
        ]:
            if speed != self._oper_data["FANSPD"]:
                self._oper_data["FANSPD"] = speed

    def set_turbo_mode(self, enable: bool):
        self._oper_data["TURBO"] = OperationMode.ON if enable else OperationMode.OFF

    def get_turbo_mode(self):
        return self._oper_data["SHABAT"] == OperationMode.ON

    def set_shabat_mode(self, enable: bool):
        self._oper_data["SHABAT"] = OperationMode.ON if enable else OperationMode.OFF

    def get_shabat_mode(self):
        return self._oper_data["SHABAT"] == OperationMode.ON

    def update_operation_states(self, data):
        self._oper_data = json.loads(data["commandJson"]["OPER"])["OPER"]
        self._time_delta = data["timeDelta"]
        measurments = json.loads(data["commandJson"]["DIAG_L2"])["DIAG_L2"]
        if "I_RAT" in measurments:
            self.collected_measure = int(measurments["I_RAT"])
        if "I_CALC_AT" in measurments:
            self.collected_measure = int(measurments["I_CALC_AT"])

        self.current_mode = measurments["O_ODU_MODE"]

    def get_operation_state(self):
        if "AC_STSRC" in self._oper_data:
            self._oper_data["AC_STSRC"] = "WI-FI"

        json_state = json.dumps({"OPER": self._oper_data})
        return json_state


if __name__=="__main__":
    imei = "2b95000057333204"
    token = "a1073694540a438ea1fa019e2e6ac68f"
    electra_api = ElectraAPI()
    electra_api.validate_token(imei, token)
    ac_dict = electra_api.get_devices()
    print(ac_dict)
    for ac in ac_dict.values():
        print(ac.name)
        print(ac.id)
        print(ac.mac)
        print(ac._oper_data)
        ac.turn_on()
        electra_api.set_state(ac)