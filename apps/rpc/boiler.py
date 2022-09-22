import socket
from enum import Enum

class BoilerState(Enum):
    OFF = 0
    ON = 1

class BoilerInterface:
    def __init__(self, server_addr=("10.100.102.23", 80)):
        self.sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.server_addr = server_addr

    def __del__(self):
        self.sock.close()

    def send_msg(self, msg):
        l = []
        for i in range(0, len(msg), 2):
            l.append(int(msg[i:i+2], 16))
        msg_in_bytes = bytes(l)
        self.sock.sendto(msg_in_bytes, self.server_addr)
        self.sock.setblocking(True)
        self.sock.settimeout(2)

    def recv_msg(self):
        try:
            resp = self.sock.recv(1024)
            return resp
        except socket.timeout:
            return None
        # resp_str = [hex(b) for b in resp]
        # print(resp_str)
        # return resp_str

    def turn_on(self):
        msg = '5aa5aa555aa5aa55000000000000000000000000000000000000000000000000abd1000039756a00de811e3dd90d43b401000000b2be00007c8bffdf60a67bdc724084a22fc47b58'
        self.send_msg(msg)

    
    def turn_off(self):
        msg = '5aa5aa555aa5aa550000000000000000000000000000000000000000000000001cd0000039756a00c6811e3dd90d43b401000000b1be0000240e72dbcf4bace4768776ad083043a6'
        self.send_msg(msg)
    
    def get_state(self):
        msg = '5aa5aa555aa5aa55000000000000000000000000000000000000000000000000b9d2000039756a00cc801e3dd90d43b401000000b0be0000d6d3248eb13bf6edf048ed4357f6fb29'
        self.send_msg(msg)
        resp = self.recv_msg()
        if resp is not None:
            if ((resp[33] & 0x10) == 0x10):
                return BoilerState.ON
            else:
                return BoilerState.OFF
        else:
            print("Error getting state")
            return None


if __name__ == "__main__":
    import time
    boiler = BoilerInterface()
    boiler.turn_on()
    time.sleep(1)
    print(boiler.get_state())
    boiler.turn_off()
    time.sleep(1)
    print(boiler.get_state())

    