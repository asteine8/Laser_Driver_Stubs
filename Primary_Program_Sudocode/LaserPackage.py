
import ConversionFunctions as convert
import Devices

import spidev
import Adafruit_ADS1x15

import time
import random


class Laser:

    # DAC Consts
    DAC_GAIN = 1 # 1x gain
    VREF_VOLTAGE = 5 # Connect VREF to +5 volts on the DAC

    # ADC Consts
    ADS1115_ADDRESS = 0x49 # Current I2C Address of the ADS1115 (find using "sudo i2cdetect -y 1")
    ADC_GAIN = 1 # FSR = +- 4.096V
    NUM_ADC_SAMPLES = 10 # Number of samples to average 



    peripheral = Devices.Peripherals # Create an object to reference the Peripherals package from

    MCP4922 = spidev.SpiDev() # Create a spi object for the DAC
    ADS1115 = Adafruit_ADS1x15.ADS1115(address=ADS1115_ADDRESS) # Create an I2C object for the ADC

    voltageData = range(2)
    opPowerData = range(2)


    def __init__(self):
        self.MCP4922.open(0,0) # Open spi port 0, device (CE) 0 (Connect to pin 24)
        self.MCP4922.max_speed_hz = 100000 # Set clk to max 100kHz (Can be higher...)


    def JumpToOpPower(self, targetPower):
        # Convert target optical power to a voltage using a preset function
        voltage = convert.OpPowerToTTLVoltage(targetPower)

        # Change TTL voltage to calculated target
        self.peripheral.WriteToDAC(self.MCP4922, 0, voltage, 1, self.VREF_VOLTAGE)

        # Record Effect on system
        opPowerData[1] = convert.self.peripheral.GetPhotodiodeVoltage(self.ADS1115, self.ADC_GAIN, self.NUM_ADC_SAMPLES)
        
    def GetDeltaOpticalPower(self, targetPower):
        # Get current optical power
        self.currentPower = convert.PhotodiodeVoltageToOpPower(self.peripheral.GetPhotodiodeVoltage(self.ADS1115, self.ADC_GAIN, self.NUM_ADC_SAMPLES))

        return targetPower - self.currentPower # Return difference (negative if under power)

    def JumpToInitialOptimization(self, targetPower):
        # 

        
