import platform
import time
import ADS1263
import RPi.GPIO as GPIO

# Define the trigger threshold
TRIGGER_THRESHOLD = 1.500
# Define the pre and post-trigger times (in seconds)
PRE_TRIGGER_TIME = 0.25
POST_TRIGGER_TIME = 0.75
# The channel to monitor
CHANNEL = 0

# Initialize the ADC
try:
    if platform.system() == "Linux":
        REF = 5.08
        ADC = ADS1263.ADS1263()
        if (ADC.ADS1263_init_ADC1('ADS1263_7200SPS') == -1):
            ADC.ADS1263_Exit()
            print("Failed to initialize ADC1")
            exit()
        ADC.ADS1263_SetMode(1)
except ImportError:
    print("ADS1263 library not available, using simulated data")

sampling_rate = 2000  # Hz
interval = 1 / sampling_rate

# Buffer to store the values
buffer = []

def read_adc():
    # Read the ADC value from the specified channel
    value = ADC.ADS1263_GetChannalValue(CHANNEL)
    # Convert the ADC value to voltage
    if value >> 31 == 1:
        voltage = -(REF * 2 - value * REF / 0x80000000)
    else:
        voltage = value * REF / 0x7fffffff
    return voltage

# Monitor the signal
while True:
    value = read_adc()
    buffer.append(value)

    # If buffer is larger than the pre-trigger samples, remove the oldest value
    if len(buffer) > PRE_TRIGGER_TIME * sampling_rate:
        buffer.pop(0)
        
    # If the value is above the trigger threshold, collect post-trigger samples
    if value >= TRIGGER_THRESHOLD:
        print(f"Trigger condition met at value: {value}")
        trigger_time = time.time()
        while time.time() - trigger_time < POST_TRIGGER_TIME:
            value = read_adc()
            buffer.append(value)
        
        # Here you can do something with the buffer
        print(buffer)
        buffer = []
        
    # Delay to match the data rate
    time.sleep(interval)
