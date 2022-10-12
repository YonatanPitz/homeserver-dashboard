import socket
import binascii

class Boiler:
    def __init__(self, server_addr=("10.100.102.23", 80)):
        self.sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.server_addr = server_addr
        self.sock.setblocking(True)
        self.sock.settimeout(2)

    def __del__(self):
        self.sock.close()

    def get_switch_state(self, id : str) -> str:
        msg = '5aa5aa555aa5aa55000000000000000000000000000000000000000000000000b9d2000039756a00cc801e3dd90d43b401000000b0be0000d6d3248eb13bf6edf048ed4357f6fb29'
        self.send_msg(msg)
        resp = self.recv_msg()
        if resp is not None:
            # print(binascii.hexlify(resp))
            # print(hex(resp[33]))
            # print(len(resp))
            # if ((resp[33] & 0x04) == 0x04):
            if resp[33] < 0xc4:
                power = "ON"
            else:
                power = "OFF"
            return {'power': power}
        else:
            print("Error getting state")
            return None

    def set_switch_state(self, id : str, state : bool):
        if state:
            self.turn_on()
        else:
            self.turn_off()

    def send_msg(self, msg):
        l = []
        for i in range(0, len(msg), 2):
            l.append(int(msg[i:i+2], 16))
        msg_in_bytes = bytes(l)
        self.sock.sendto(msg_in_bytes, self.server_addr)

    def recv_msg(self):
        try:
            resp = self.sock.recv(1024)
            return resp
        except socket.timeout:
            return None

    def turn_on(self):
        msg = '5aa5aa555aa5aa55000000000000000000000000000000000000000000000000abd1000039756a00de811e3dd90d43b401000000b2be00007c8bffdf60a67bdc724084a22fc47b58'
        self.send_msg(msg)

    
    def turn_off(self):
        msg = '5aa5aa555aa5aa550000000000000000000000000000000000000000000000001cd0000039756a00c6811e3dd90d43b401000000b1be0000240e72dbcf4bace4768776ad083043a6'
        self.send_msg(msg)



if __name__ == "__main__":
    import time
    boiler = Boiler()
    for i in range(10):
        print(boiler.get_switch_state(0))
        time.sleep(1)
    print("turn on")
    boiler.turn_on()
    for i in range(10):
        print(boiler.get_switch_state(0))
        time.sleep(1)
    print(boiler.get_switch_state(0))
    print("turn off")
    boiler.turn_off()
    for i in range(10):
        print(boiler.get_switch_state(0))
        time.sleep(1)

    