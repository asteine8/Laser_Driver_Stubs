"""
Phillia Steiner, 2018
FU630Laser.py
This package allows one to interface with a FU-630SLD pump laser utilizing the ADS1115 ADC and the MCP4922 DAC modules. Four pump lasers can be attached at once due to the limited number of spi CE ports (two count).
"""

import ConversionFunctions as convert
import Devices

import spidev
import Adafruit_ADS1x15

import time
# import random

class FU630_Laser:

    # DAC Consts
    DAC_PORT = 0 # Port 0 for spi (default)
    DAC_CE = 0 # CE pin for DAC (Chip Enable)
    DAC_SPI_SPEED = 100000 # Clock speed for DAC spi comms (100kHz is good)
    DAC_GAIN = 1 # 1x gain
    VREF_VOLTAGE = 3.3 # Connect VREF to +3.3 volts on the DAC

    TTL_DAC_CHANNEL = 0 # 0 = channel A, 1 = channel B

    # ADC Consts
    ADS1115_ADDRESS = 0x49 # Current I2C Address of the ADS1115 (find using "sudo i2cdetect -y 1")
    ADC_GAIN = 1 # FSR = +- 4.096V
    NUM_ADC_SAMPLES = 10 # Number of samples to average

    TTL_ADC_CHANNEL = 0 # Standard channel (No Differential)
    PHOTODIODE_ADC_CHANNEL = 1 # Standard channel (No Differential)
    PHOTODIODE_SHUNT_RESISTANCE = 1000 # Should be 1k, value shoud be experimentally determined

    peripheral = Devices.Peripherals # Create an object to reference the Peripherals package from

    MCP4922 = spidev.SpiDev() # Create a spi object for the DAC
    ADS1115 = Adafruit_ADS1x15.ADS1115(address=ADS1115_ADDRESS) # Create an I2C object for the ADC

    NUM_DATA_POINTS = 3 # Number of data points to store (Only really need 2 but 3 are taken just in case)
    voltageData = list(range(NUM_DATA_POINTS)) # Store three data points (one extra for later use)
    opPowerData = list(range(NUM_DATA_POINTS))

    targetOpPower = 0 # The optical power output (in mW) that is continuously optimized to

    def __init__(self): # Do on class initialization
        self.MCP4922.open(self.DAC_PORT, self.DAC_CE) # Open spi port 0, device (CE) 0 (Connect to pin 24)
        self.MCP4922.max_speed_hz = self.DAC_SPI_SPEED # Set clk to max 100kHz (Can be higher...)
        self.optimizationState = 0
        self.functionList = [self.JumpToOpPower, self.JumpToInitialOptimization, self.ApplyTwoPointOptimization]

    def GetDeltaOpticalPower(self, targetPower):
        # Get current optical power
        self.currentPower = convert.PhotodiodeVoltageToOpPower(self.peripheral.GetPhotodiodeVoltage(self.ADS1115, self.PHOTODIODE_ADC_CHANNEL, self.ADC_GAIN, self.NUM_ADC_SAMPLES), self.PHOTODIODE_SHUNT_RESISTANCE)

        return targetPower - self.currentPower # Return difference (negative if under power)

    def RecordData(self):
        # Record Effects on system via photodiode and TTL voltage using ADC and push data up through lists
        
        for i in range(self.NUM_DATA_POINTS-1,0,-1): # Shift up elements one index
            self.opPowerData[i] = self.opPowerData[i-1]
            self.voltageData[i] = self.voltageData[i-1]
        
        # Shuffle new data in at index 0
        self.opPowerData[0] = convert.PhotodiodeVoltageToOpPower(self.peripheral.GetPhotodiodeVoltage(self.ADS1115, self.PHOTODIODE_ADC_CHANNEL, self.ADC_GAIN, self.NUM_ADC_SAMPLES), self.PHOTODIODE_SHUNT_RESISTANCE)
        self.voltageData[0] = self.peripheral.GetTTLVoltage(self.ADS1115, self.TTL_ADC_CHANNEL, self.ADC_GAIN, self.NUM_ADC_SAMPLES)

    def JumpToOpPower(self, targetPower):
        # Convert target optical power to a voltage using a preset function
        voltage = convert.OpPowerToTTLVoltage(targetPower)

        # Change TTL voltage to calculated target
        self.peripheral.WriteToDAC(self.MCP4922, self.TTL_DAC_CHANNEL, voltage, self.DAC_GAIN, self.VREF_VOLTAGE)

        self.RecordData() # Record state of system

    def JumpToInitialOptimization(self, targetPower):
        # Use linear approximation with the computed point slope on the optical power / voltage curve

        # Calculate voltage to write to DAC (index 0 of data storage always references last data point)
        voltage = (targetPower - self.opPowerData[0]) / convert.PowerOverVoltageSlopeAtPower(self.opPowerData[0]) + self.voltageData[0]

        self.peripheral.WriteToDAC(self.MCP4922, self.TTL_DAC_CHANNEL, voltage, self.DAC_GAIN, self.VREF_VOLTAGE)
        
        self.RecordData() # Record state of system

    def ApplyTwoPointOptimization(self, targetPower):
        # Uses previous two data points to optimize current system to a target optical power output utilizing linear regression methods

        # Calculate the slope between the previous two points
        m = (self.opPowerData[1] - self.opPowerData[0]) / (self.voltageData[1] - self.voltageData[0])

        # Calculate new target voltage
        voltage = (targetPower - self.opPowerData[0]) / m + self.voltageData[0]

        # Write new voltage to DAC TTL port
        self.peripheral.WriteToDAC(self.MCP4922, self.TTL_DAC_CHANNEL, voltage, self.DAC_GAIN, self.VREF_VOLTAGE)

        self.RecordData() # Record state of system
    
    def ModifyOptimizationState(self):
        if self.optimizationState < len(self.functionList) - 1:
            self.optimizationState += 1

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # User Functions (The only functions a user really needs to use)

    def SetTargetOpticalPower(self, targetPower):
        # Function to set target optical power to enhance readability of user code
        self.targetOpPower = targetPower
        self.optimizationState = 0 # Reset optimization state

    def OptimizeOpticalPower(self):
        # optimize to set optical power target
        self.functionList[self.optimizationState](self.targetOpPower) # Call appropiate function with target optical power
        self.ModifyOptimizationState() # Change the optimization State
    

