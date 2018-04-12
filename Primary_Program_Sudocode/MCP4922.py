
# import spidev

def WriteToDAC(device, channel, data, gain):
    # Writes to and turns on selected channel
    # Gain settings:
    #   >>1 = 1x gain
    #   >>0 = 2x gain

    bytesOut = [0,0] # Preallocate as local variable

    bytesOut[0] |= (channel << 7) | (gain << 5) # select channel and gain
    bytesOut[0] |= (1 << 4) # Don't shutdown the channel

    bytesOut[1] = data & 255 # Use 255 as 8 bit bitmask to get first 8 bits of data
    bytesOut[0] |= ((data >> 8) & 15) # Use 15 as 4 bit bitmask to get last 4 bits of data

    # device.xfer2(bytesOut) # Write Bytes to DAC
    print(bin(bytesOut[1]))
    print(bin(bytesOut[0]))


def DeactivateDAC(device, channel):
    bytesOut = [0,0] # Preallocate as local variable

    bytesOut[0] |= (0 << 4) | (channel << 7) # Write a 0 to the SHDN bit and select channel
    
    # device.xfer2(bytesOut) # Write Bytes to DAC
    print("DAC Off")

def ConvertVoltageToDACValue(voltage, vRef):
    return voltage / vRef * 4096