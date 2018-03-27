
# MOSI to pin 19, CLK to pin 23, CS to pin 24

import math # Import math package
import spidev # Import SPI package

spi = spidev.SpiDev() # Create Spi Object

gain = 1 # Gain is 1

def Int2Bytes(integer):
    # Convert int datatype into "bytes" datatype
    if integer < 0:
        integer *= -1 # Convert to positive number

    bits = len(bin(integer)) # Get number of bits in integer
    bOuts = bytes([0])
    bOuts *= math.ceil(bits/8) # Extend array to encompass entire integer

    for i in range( len(bOuts) ):
        bOuts(len(bOuts)-i-1) |= (integer >> (8 * i)) & 256

    return bOuts
    

def WriteToDAC(channel,data,onOff):

    bytesOut = bytes([0,0])

    if onOff: # Write 0 to register and a 1 to SHDN to turn off channel
        bytesOut(1) |= (0 << 4) | (channel << 7) # Write a 0 to the SHDN bit and select channel
        
        spi.writebytes(bytesOut) # Write Bytes to DAC

    bytesOut(1) |= (channel << 7) | (gain << 5) # select channel and gain
    bytesOut(1) |= (1 << 4) # Don't shutdown the channel



    



spi.open(0,0)  # Open spi port 0, device (CE) 0 (Connect to pin 24)

