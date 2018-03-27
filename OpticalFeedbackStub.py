import RPi.GPIO as GPIO # GPIO Library for Raspberry Pi

def WriteVoltageToDAC(vOut): # Writes voltage to attached DAC
    # Convert Voltage to decimal form for output

    # Write data to DAC

    if written:
        return 1 # Write successful
    else:
        return 0 # Write failed

def GetOpticalPower(): # Returns optical power from on-chip photodiode

    # Communicate with ADC to read voltage over photodiode shunt

    # Convert photodiode shunt voltage to optical power
    return power

def ConvPow2Volt(oPower): # Converts optical power to estimated voltage

    # Use inverse function of P(v) (P(v)')

    return voltage
    
def ConvPow2

def JumpToPower(oPower): # Sets TTL voltage to calculated value to reach desired optical power

    # Convert oPower (optical power) to theoretical voltage out using Power(voltage)' function

    return WriteVoltageToDAC(targetJumpVoltage) # Return success bit

def ApproximateToPower(iteration, ):





