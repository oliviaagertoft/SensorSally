import time
import sys
sys.path.insert(0,'../libs/DFRobot_ADS1115/RaspberryPi/Python/')
sys.path.insert(0,'../src/')

from DFRobot_ADS1115 import ADS1115
from GreenPonik_EC import GreenPonik_EC

ADS1115_REG_CONFIG_PGA_6_144V = 0x00  # 6.144V range = Gain 2/3
ADS1115_REG_CONFIG_PGA_4_096V = 0x02  # 4.096V range = Gain 1
ADS1115_REG_CONFIG_PGA_2_048V = 0x04  # 2.048V range = Gain 2 (default)
ADS1115_REG_CONFIG_PGA_1_024V = 0x06  # 1.024V range = Gain 4
ADS1115_REG_CONFIG_PGA_0_512V = 0x08  # 0.512V range = Gain 8
ADS1115_REG_CONFIG_PGA_0_256V = 0x0A  # 0.256V range = Gain 16

ads1115 = ADS1115()
ec = GreenPonik_EC()
ec.begin()


def calibration():
    global ads1115
    global ec
    temperature = 25 # or make your own temperature read method
    # Set the IIC address
    ads1115.set_addr_ADS1115(0x48)
    # Sets the gain and input voltage range.
    ads1115.set_gain(ADS1115_REG_CONFIG_PGA_6_144V)
    # Get the Digital Value of Analog of selected channel
    adc0 = ads1115.read_voltage(0)
    return ec.calibration(adc0['r'], temperature)


if __name__ == "__main__":
    while True:
        calibration()
        time.sleep(1)

