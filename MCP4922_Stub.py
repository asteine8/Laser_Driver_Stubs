# MCP4922 Test code for interfacing the MCP4922 12 bit digital to analog converter with the Raspberry Pi 2
# Phillia Steiner - March 27, 2018

# Connect:
# Vcc to +3.3v, and one GND pin to GND
# SDI to pin 19 (MOSI), SCLK to pin 23 (SPI CLK), CS to pin 24 (CE0), LDAC to GND, SHDN to Vcc
# Note that Vref should be between Vcc and GND


# WriteToDAC(channel,data,isOn)
# 
# "channel" selects between the DAC output to write to
#       0 - Write to channel A
#       1 - Write to channel B
# ---
# "data" is the dac value to write to the selected channel
#       Should be a positive integer value between 0 and 2^12-1 (4095)
# ---
# "isOn" changes the on/off state of the selected DAC channel
#       0 - Shuts down the selected DAC channel (Reduces power consumption)
#       1 - Enables the selected DAC channel
# ---
# Vout = Vref* data/4095 where data is a base 10 value

import spidev # Import SPI package - unique to the raspberry pi
import sys
import time

spi = spidev.SpiDev() # Create Spi Object

gain = 1 # Gain is 1x, can be changed to 0 to get a 2x gain

Vcc = 3.3 # Input voltage
    

def WriteToDAC(channel,data,isOn):

    bytesOut = [0,0] # Preallocate as local variable

    if not isOn: # Write 0 to register and a 1 to SHDN to turn off channel
        bytesOut[0] |= (0 << 4) | (channel << 7) # Write a 0 to the SHDN bit and select channel
        
        spi.xfer2(bytesOut) # Write Bytes to DAC

    bytesOut[0] |= (channel << 7) | (gain << 5) # select channel and gain
    bytesOut[0] |= (1 << 4) # Don't shutdown the channel

    bytesOut[1] = data & 255 # Use 255 as 8 bit bitmask to get first 8 bits of data
    bytesOut[0] |= ((data >> 8) & 15) # Use 15 as 4 bit bitmask to get last 4 bits of data

    spi.xfer2(bytesOut) # Write Bytes to DAC

sys.stdout.write("Initializing\n")
spi.open(0,0)  # Open spi port 0, device (CE) 0 (Connect to pin 24)
spi.max_speed_hz = 100000 # Set clk to max 100kHz (Can be higher...)

voltage = input("Enter Target Voltage: ")
WriteToDAC(1, round(voltage/Vcc*4096), 0)


