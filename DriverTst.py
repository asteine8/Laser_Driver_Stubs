import FU630Driver
import time

testLaser = FU630Driver.FU630Laser.FU630_Laser() # Create a FU630_Laser object


powpow = input("Enter Target Optical Power (mW):") # Request target optical power
testLaser.SetTargetOpticalPower(powpow) # Set target for optical power

print("")

numOptimizations = 0 # Start unoptimized

while True: # Optimize endlessly (use Ctrl + z to stop)
    testLaser.OptimizeOpticalPower() # Appy optical power optimization
    numOptimizations += 1 # Increment up number of optimizations

    # Print out sensory data to console
    print(str(testLaser.voltageData[0]) + " | " + str(testLaser.opPowerData[0]))

    # Print the number of optimizations
    print(str(numOptimizations) + "\n")

    # Wait for a second
    time.sleep(1)