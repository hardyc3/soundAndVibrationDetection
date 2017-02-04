import smbus

class LCD:
    
    def __init__(self, device_address):
        self.bus = smbus.SMBus(1)
        self.addr = device_address

