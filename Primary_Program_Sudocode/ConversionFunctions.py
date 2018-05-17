
def TTLVoltageToOpPower(voltage):
    # Function to convert measured ttl voltage to optical power
    return voltage * 20

def OpPowerToTTLVoltage(power):
    # Function to convert measured optical power to ttl voltage
    return power / 20

def PowerOverVoltageSlopeAtPower(power):
    # Returns the slope of power over voltage at a point defined by optical power
    return 2 * power

def PhotodiodeVoltageToOpPower(voltage):
    # Function to convert measured photodiode voltage to optical power
    return voltage