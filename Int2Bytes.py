import sys
import math

def Int2Bytes(integer):
    intVal = int(integer)
    # Convert int datatype into "bytes" datatype
    if intVal < 0:
        intVal *= -1 # Convert to positive number

    bits = len(bin(intVal)) # Get number of bits in intVal

    bOuts = [0]
    bOuts *= math.ceil(bits/8) # Extend array to encompass entire integer

    for i in range(len(bOuts)):
        
        bOuts[len(bOuts)-i-1] |= (intVal >> (8 * i))

    return bOuts

def PrintBytes(byts):

    for i in range(len(byts)):
        
        for b in range(8):

            sys.stdout.write( str((byts[i] >> (8-b-1)) & 1) )
        
    print("")

    




# print(str(Int2Bytes(2**17)).format(37))
for i in range(16):
    a = 1+ 10*i
    PrintBytes(Int2Bytes(a))
    print(bin(a))
    print("")