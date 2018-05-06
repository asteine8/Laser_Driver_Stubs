
import Adafruit_ADS1x15
import time

ADS1115_ADDRESS = 0x49 # Current I2C Address of the ADS1115 (find using "sudo i2cdetect -y 1")
# gain = 1 # FSR = +- 4.096 V
# gain = 4 # FSR = +- 1.024 V
gain = 16 # FSR = +- 0.256 V
dataRate = 860

def ConvertToVoltage(reading, adcGain):
    if adcGain == 1:
        return reading * 0.000125
    elif adcGain == 2:
        return reading * 0.0000625
    elif adcGain == 4:
        return reading * 0.00003125
    elif adcGain == 8:
        return reading * 0.000015625
    elif adcGain == 16:
	    return reading * 0.0000078125


ADS1115 = Adafruit_ADS1x15.ADS1115(address=ADS1115_ADDRESS) # Declare ADS1115 as our adc object

ADS1115.start_adc_difference(0,gain,dataRate) # Initialize ADC in continuous conversion mode 
# ADC channels started in a differential input channel 0 minus channel 1

while 1:
    runSum = 0 # Preallocate running sum variable
    numSamples = 50
    for i in range(numSamples): # iterate for each sample
        # data = ADS1115.get_last_result()
        # runSum += data
        # print(data)
        runSum += ADS1115.get_last_result() # Sum with aquired data

    aveVolts = ConvertToVoltage(runSum/numSamples, gain) # Get average voltage
    print(aveVolts) # Output average voltage to console
    time.sleep(0.2) # Wait a bit to prevent a stack overflow with the print function

