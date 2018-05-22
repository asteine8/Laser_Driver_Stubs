import math

def TTLVoltageToOpPower(voltage):
    # Function to convert measured ttl voltage (volts) to optical power (mW)
    return 481*voltage - 630 - 79.8*(voltage**2)

def OpPowerToTTLVoltage(power):
    # Function to convert measured optical power to ttl voltage
    return (1/798)*(2405 - math.sqrt(756625-7980*power))

def PowerOverVoltageSlopeAtPower(power):
    # Returns the slope of power over voltage at a point defined by optical power
    voltage = OpPowerToTTLVoltage(power)
    return 481 - 159.6 *  voltage

def PhotodiodeVoltageToCurrent(voltage, shuntResistance):
    # Function to convert a measured voltage to current given the shunt resitance
    return voltage / shuntResistance

def PhotodiodeVoltageToOpPower(voltage, shuntResistance):
    # Function to convert measured photodiode voltage to optical power (mW)
    current = PhotodiodeVoltageToCurrent(voltage, shuntResistance)
    return 140 * current + 1.57