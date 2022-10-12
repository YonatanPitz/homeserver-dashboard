from django.conf import settings
from apps.rpc.switch_intf import SwitchInterface

import socket
import time
import time
from struct import pack
from binascii import crc_hqx, hexlify, unhexlify

def current_timestamp_to_hexadecimal() -> str:
    """Generate hexadecimal representation of the current timestamp.
    Return:
        Hexadecimal representation of the current unix time retrieved by ``time.time``.
    """
    round_timestamp = int(round(time.time()))
    binary_timestamp = pack("<I", round_timestamp)
    hex_timestamp = hexlify(binary_timestamp)
    return hex_timestamp.decode()

def sign_packet_with_crc_key(hex_packet: str) -> str:
    """Sign the packets with the designated crc key.
    Args:
        hex_packet: packet to sign.
    Return:
        The calculated and signed packet.
    """
    binary_packet = unhexlify(hex_packet)
    binary_packet_crc = pack(">I", crc_hqx(binary_packet, 0x1021))
    hex_packet_crc = hexlify(binary_packet_crc).decode()
    hex_packet_crc_sliced = hex_packet_crc[6:8] + hex_packet_crc[4:6]

    binary_key = unhexlify(hex_packet_crc_sliced + "30" * 32)
    binary_key_crc = pack(">I", crc_hqx(binary_key, 0x1021))
    hex_key_crc = hexlify(binary_key_crc).decode()
    hex_key_crc_sliced = hex_key_crc[6:8] + hex_key_crc[4:6]

    return hex_packet + hex_packet_crc_sliced + hex_key_crc_sliced


class Switcher(SwitchInterface):
    def __init__(self):
        super().__init__()
        # TODO: Fill this in automatically with discovery
        self.device_ids_and_ips = {
            "9abb1f": "10.100.102.21"
        }
        self.port = 9957
    
    def _login(self, s):
        timestamp = current_timestamp_to_hexadecimal()
        login_packet = f"fef052000232a10000000000340001000000000000000000{timestamp}00000000000000000000f0fe1c" + "0" * 74
        signed_packet = sign_packet_with_crc_key(login_packet)
        s.send(unhexlify(signed_packet))
        response = s.recv(1024)
        return hexlify(response)[16:24].decode(), timestamp

    def _send_resp(self, s, packet):
        signed_packet = sign_packet_with_crc_key(packet)
        s.send(unhexlify(signed_packet))
        state_resp = s.recv(1024)
        hex_response = hexlify(state_resp)
        return hex_response[150:152].decode()

    def get_switch_state(self, id : str) -> bool:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if id not in self.device_ids_and_ips:
            print(f"Recieved unrecognized device id {id}")
        ip = self.device_ids_and_ips[id]
        s.connect((ip, self.port))
        session_id, timestamp = self._login(s)
        get_state_packet = f"fef0300002320103{session_id}340001000000000000000000{timestamp}00000000000000000000f0fe{id}00"
        hex_state = self._send_resp(s, get_state_packet)
        s.close()
        if hex_state == "01":
            return {'power': 'ON'}
        elif hex_state == "00":
            return {'power': 'OFF'}


    def set_switch_state(self, id : str, state : bool):
        if id not in self.device_ids_and_ips:
            print(f"Recieved unrecognized device id {id}")
        ip = self.device_ids_and_ips[id]
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip, self.port))
        session_id, timestamp = self._login(s)
        if state:
            command = "1"
        else:
            command = "0"
        turn_on_packet = f"fef05d0002320102{session_id}340001000000000000000000{timestamp}00000000000000000000f0fe{id}" + "0" * 72 + f"000106000{command}0000000000"
        self._send_resp(s, turn_on_packet)
        s.close()