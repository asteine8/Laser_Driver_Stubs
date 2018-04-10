

import smbus # Package for I2C Comms

# Keep commented out unless needed
# import time
# import math

# ADS1115 7 bit address
ADS1115_ADDRESS = 0x49

# Register Values
ADS1115_CONV_REG = 0x00
ADS1115_CONFIG_REG = 0x01
ADS1115_LO_THRESH_REG = 0x02
ADS1115_HI_THRESH_REG = 0x03


# Note: The ADS1115 should be run in continuous conversion mode - starts new converstion as soon as the previous data is read

I2CBus = smbus.SMBus(1) # Connect to I2C port 1

def configureADS1115(addr,ampMode,opMode,dataRate):
    # Amplification Modes:
    #   -5 = +-0.256 V
    #   -4 = +-0.512 V
    #   -3 = +-1.024 V
    #   -2 = +-2.048 V
    #   -1 = +-4.096 V
    #   -0 = +-6.144 V
    # 
    # Device Operation Modes
    #   -0 = Continuous-conversion mode
    #   -1 = Single-shot mode or power-down state (default)
    # 
    # Data Rate Modes (Samples per Second):
    #   -0 = 8 SPS
    #   -1 = 16 SPS
    #   -2 = 32 SPS
    #   -3 = 64 SPS
    #   -4 = 128 SPS (default)
    #   -5 = 250 SPS
    #   -6 = 475 SPS
    #   -7 = 860 SPS
    # 
    # Most significant byte should be written to the config register first

    configBytes = [0,0]

    configBytes[1] |= (ampMode << 1) # Set amplification mode
    configBytes[1] |= (opMode) # Set operation mode
    configBytes[0] |= (dataRate << 5) # Set data rate

    # Write to configuration register with given settings
    I2CBus.write_i2c_block_data(addr, ADS1115_CONFIG_REG, configBytes)

def setADS1115PinMUX(addr, MUX):
    # MUX Settings
    # 0 : AINP = AIN0 and AINN = AIN1 (default)
    # 1 : AINP = AIN0 and AINN = AIN3
    # 2 : AINP = AIN1 and AINN = AIN3
    # 3 : AINP= AIN2 and AINN = AIN3
    # 4 : AINP = AIN0 and AINN = GND
    # 5 : AINP = AIN1 and AINN = GND
    # 6 : AINP = AIN2 and AINN = GND
    # 7 : AINP = AIN3 and AINN = GND
    readADS1115Reg(ADS1115_ADDRESS,ADS1115_CONFIG_REG)

def readADS1115Reg(addr, register):

    I2CBus.write_byte(addr, register) # Prepare to read "register"

    dataOut = [0,0]

    dataOut = I2CBus.read_i2c_block_data(addr)

    return dataOut

