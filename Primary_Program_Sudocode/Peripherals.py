
import ADS1115
import MCP4922

# Constant Declarations
ADS1115_ADDRESS = 0x49
TTL_ADC_CHANNEL = 3 # ADS1115 channel 3 for the library coresponds to a differential adc input of channel 2 minus channel 3
PHOTO_ADC_CHANNEL = 0 # ADS1115 channel 0 for the library coresponds to a differential adc input of channel 0 minus channel 1


def Voltage(power):
    # A function to convert optical power to voltage
    voltage = power
    return voltage

def OpPower(voltage):
    # A function to convert voltage
    power = voltage
    return power

def GetTTLVoltage(device, gain, numSamples):
    # A function to return the average of "numSamples" readings with a set gain
    runSum = 0

    for i in range(numSamples):
        runSum += ADS1115.ReadFromADCDifferntial(device, TTL_ADC_CHANNEL, gain)
    
    return ADS1115.ConvertToVoltage(runSum/numSamples, gain)

def GetPhotodiodeVoltage(device, gain, numSamples):

    runSum = 0

    for i in range(numSamples):
        runSum += ADS1115.ReadFromADCDifferntial(device, PHOTO_ADC_CHANNEL, gain)
    
    return ADS1115.ConvertToVoltage(runSum/numSamples, gain)

def WriteToDAC(spiDevice, channel, voltage, gain, vRefVoltage):

    DACData = MCP4922.ConvertVoltageToDACValue(voltage, vRefVoltage)

    MCP4922.WriteToDAC(spiDevice, channel, DACData, gain)


