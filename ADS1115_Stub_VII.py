
import Adafruit_ADS1x15
import time

ADS1115_ADDRESS = 0x49
gain = 1
dataRate = 860

ADS1115 = Adafruit_ADS1x15.ADS1115(address=ADS1115_ADDRESS) # Declare ADS1115 as our adc object

ADS1115.start_adc(0,gain,dataRate) # Initialize ADC in continuous conversion mode measuring off channel 1

adcData = range(100)
for i in range(100):
    adcData[i] = ADS1115.get_last_result() # Gets latest result stored in ADC register
    time.sleep(0.05) # Wait a bit (No point in going faster...

for i in range(100):
    print(adcData[i])




