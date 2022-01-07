import struct
import smbus
import RPi.GPIO as GPIO


class UPS_PW(object):
    """class for UPS_Lite with MAX17040."""

    def __init__(self, i2c=1, addr=0x36):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(4,GPIO.IN)
        # 0 = /dev/i2c-0 (port I2C0), 1 = /dev/i2c-1 (port I2C1)
        self._bus = smbus.SMBus(i2c)
        self._address = addr

    def QuickStart(self):
        self._bus.write_word_data(self._address, 0x06, 0x4000)

    def PowerOnReset(self):
        self._bus.write_word_data(self._address, 0xfe, 0x0054)

    """This function returns as float the voltage from the Raspi UPS Hat via the provided SMBus object"""
    def readVoltage(self):
        read = self._bus.read_word_data(self._address, 0X02)
        swapped = struct.unpack("<H", struct.pack(">H", read))[0]
        voltage = swapped * 1.25 /1000/16
        return voltage

    """This function returns as a float the remaining capacity of the battery connected to the Raspi UPS Hat via the provided SMBus object"""
    def readCapacity(self):
        read = self._bus.read_word_data(self._address, 0X04)
        swapped = struct.unpack("<H", struct.pack(">H", read))[0]
        capacity = swapped/256
        return capacity

    def getPowerStatus(self):
        return (GPIO.input(4) == GPIO.HIGH)

    def Init(self):
        """Initialize MAX17040"""
        self.PowerOnReset()
        self.QuickStart()
        # time.sleep(1)


if __name__ == '__main__':
    import time
    ups = UPS_PW()
    ups.Init()
    time.sleep(1)

    print("++++++++++++++++++++")
    print("Voltage:%5.2fV" % ups.readVoltage())
    print("Battery:%5i%%" % ups.readCapacity())

    if ups.readCapacity() == 100:
        print("Battery FULL")
    elif ups.readCapacity() < 5:
        print("Battery LOW")

    if ups.getPowerStatus():
        print("Power Adapter Plug In ")
    else:
        print("Power Adapter Unplug")

    print("++++++++++++++++++++")

