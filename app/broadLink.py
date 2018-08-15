import broadLingLib


class BroadLinkDevice():
    def __connect(self):
        try:
            if self.__devType == 'SP2' or self.__devType == 'SP1':
                self.__device = broadLingLib.gendevice(
                    0x2711, (self.__ip, 80), bytearray.fromhex(self.__mac))
            if self.__devType == 'SP3S':
                self.__device = broadLingLib.gendevice(
                    0x947a, (self.__ip, 80), bytearray.fromhex(self.__mac))
                self.hasPowerMonitor = True

            if self.__device is not None:
                self.__device.auth()
                self.__isConnected = True
                return (True, "")
        except Exception as e:
            self.__isConnected = False
            print(e)
            return (False, "")

    def __checkPower(self):
        try:
            state = self.__device.check_power()
        except Exception as e:
            return (False, str(e))
        return (True, state)

    def __getEnergy(self):
        try:
            energy = self.__device.get_energy()
        except Exception as e:
            return (False, str(e))
        return (True, energy)

    def __turnOnOff(self, operation):
        try:
            self.__device.set_power(operation)
            state = self.__device.check_power()
        except Exception as e:
            return (False, str(e))
        return (True, state)

    def __init__(self, ip, mac, devType):
        self.__ip = ip
        self.__mac = mac
        self.__device = None
        self.__devType = devType
        self.__isConnected = False
        self.hasPowerMonitor = False

    def is_On(self):
        if not self.__isConnected:
            self.__connect()
        if self.__isConnected:
            return self.__checkPower()
        return (False, "JMN: Unable to connect")

    def on(self):
        if not self.__isConnected:
            self.__connect()
        if self.__isConnected:
            return self.__turnOnOff(True)
        return (False, "JMN: Unable to connect")

    def off(self):
        if not self.__isConnected:
            self.__connect()
        if self.__isConnected:
            return self.__turnOnOff(False)
        return (False, "JMN: Unable to connect")

    def getPower(self):
        if not self.__isConnected:
            self.__connect()
        if self.__isConnected:
            return self.__getEnergy()
        return (False, "JMN: Unable to connect")
