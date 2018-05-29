import math

# All voltages should be in volts
# All Currents should be in milliamperes (mA)
# All optical powers should be in milliwatts (mW)

def TTLVoltageToOpPower(voltage):
    # Function to convert measured ttl voltage (volts) to optical power (mW) - based on experimental data R^2 = 0.999
    if voltage > 3.0138:
        return 94.8 # Function fails to model higher voltages
    else:
        return 481*voltage - 630 - 79.8*(voltage**2) # Apply modeling function

def OpPowerToTTLVoltage(power):
    # Function to convert measured optical power (mW) to ttl voltage (volts) - based on experimental data R^2 = 0.999
    if power > 94.8:
        return 3 # Function does not model for optical power above 94.8 mW
    else:
        return (1/798)*(2405 - math.sqrt(756625-7980*power)) # Apply modeling function

def PowerOverVoltageSlopeAtPower(power):
    # Returns the slope of power over voltage (volts) at a point defined by optical power (mW)
    voltage = OpPowerToTTLVoltage(power)
    return 481 - 159.6 *  voltage

def PhotodiodeVoltageToCurrent(voltage, shuntResistance):
    # Function to convert a measured voltage (volts) to current (mA) given the shunt resitance
    return 1000 * voltage / shuntResistance # Multiply by 1000 to convert Amps to mA

def PhotodiodeVoltageToOpPower(voltage, shuntResistance):
    # Function to convert measured photodiode voltage (volts) to optical power (mW) - based on experimental data R^2 = 1.000
    current = PhotodiodeVoltageToCurrent(voltage, shuntResistance)
    return 140 * current + 1.57