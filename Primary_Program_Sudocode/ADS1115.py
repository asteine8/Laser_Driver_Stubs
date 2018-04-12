# import Adafruit_ADS1x15

import random

def ReadFromADCDifferntial(device, channel, gain):
    # Gets data from the ADS1115 with variable channel and gain

    return device.read_adc_difference(channel, gain)

    return random.randint(-2**15,2**15)

def ConvertToVoltage(data, gain):
    # Converts ADS1115 signed data to a voltage value based on the gain of the reading

    if gain == 1:
        return data * 0.000125
    elif gain == 2:
        return data * 0.0000625
    elif gain == 4:
        return data * 0.00003125
    elif gain == 8:
        return data * 0.000015625
    elif gain == 16:
	    return data * 0.0000078125