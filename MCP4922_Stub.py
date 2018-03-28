
# MOSI to pin 19, CLK to pin 23, CS to pin 24, LDAC to GND

import math # Import math package
import spidev # Import SPI package
import time

spi = spidev.SpiDev() # Create Spi Object

gain = 1 # Gain is 1x
    

def WriteToDAC(channel,data,on):

    bytesOut = [0,0]

    if not on: # Write 0 to register and a 1 to SHDN to turn off channel
        bytesOut[0] |= (0 << 4) | (channel << 7) # Write a 0 to the SHDN bit and select channel
        
        spi.xfer2(bytesOut) # Write Bytes to DAC

    bytesOut[0] |= (channel << 7) | (gain << 5) # select channel and gain
    bytesOut[0] |= (1 << 4) # Don't shutdown the channel

    bytesOut[1] = data & 255 # Use 255 as 8 bit bitmask to get first 8 bits of data
    bytesOut[0] |= ((data >> 8) & 15) # Use 15 as 4 bit bitmask to get last 4 bits of data

    #print(bin(bytesOut[0]))
    #print(bin(bytesOut[1]))
    #print("")
    spi.xfer2(bytesOut)


spi.open(0,0)  # Open spi port 0, device (CE) 0 (Connect to pin 24)
spi.max_speed_hz = 100000 # Set clk to max 16MHz
		
while 1:
	for i in range(0, 4096, 2):

		WriteToDAC(0,i,1)