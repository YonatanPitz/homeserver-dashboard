import serial
import time

class CielFan:
    def __init__(self, id):
        self.id = id
        self.ser = serial.Serial(port="/dev/ttyACM0", baudrate=9600, timeout=1)
        time.sleep(0.3)

    def __del__(self):
        self.ser.close()
    
    def send_cmd_bytes(self, cmd_bytes):
        print("sending cmd:")
        print(cmd_bytes)
        self.ser.write(cmd_bytes)
        time.sleep(0.3)
        print("response:")
        print(self.ser.read(80))
        self.ser.close()

    def send_cmd(self, cmd):
        cmd_bytes = str(int(self.id+cmd, 16)).encode()
        self.send_cmd_bytes(cmd_bytes)

    def set_light(self, light):
        if light == "ON":
            self.send_cmd("110")
        if light == "OFF":
            self.send_cmd("1E0")
    
    def set_fan(self, fan):
        if fan == "HIGH":
            self.send_cmd("180")
        if fan == "MED":
            self.send_cmd("140")
        if fan == "LOW":
            self.send_cmd("1C0")
        if fan == "OFF":
            self.send_cmd("190")

if __name__ == "__main__":
    ciel = CielFan(id="0xe7d")
    ciel.set_light("ON")