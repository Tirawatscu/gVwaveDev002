import platform
import time
import ADS1263
import RPi.GPIO as GPIO
import bluetooth

# Define the trigger threshold
TRIGGER_THRESHOLD = 0.3
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

sampling_rate = 1000  # Hz
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

# Set up Bluetooth connection
server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
port = 1
server_sock.bind(("", port))
server_sock.listen(1)
print("Listening for connections on RFCOMM channel", port)
client_sock, address = server_sock.accept()
print("Accepted connection from", address)

def send_data_over_bluetooth(data):
    print(f"Send {len(data)} sample")
    # Convert data to string format and join them into a single string
    string_data = 'START\n' + ','.join(map(str, data)) + '\nEND'
    # Convert the string to bytes
    byte_data = string_data.encode('utf-8')

    # Chunk size
    chunk_size = 12800  # You can adjust this value

    # Send the byte data in chunks
    for i in range(0, len(byte_data), chunk_size):
        total_sent = 0
        while total_sent < len(byte_data[i:i+chunk_size]):
            sent = client_sock.send(byte_data[i:i+chunk_size][total_sent:])
            if sent == 0:
                raise RuntimeError("socket connection broken")
            total_sent = total_sent + sent
        #time.sleep(0.1)

def collect_adc_data(duration):
    ADC_Value_List = []
    start_time = time.time()
    no_sample = duration * sampling_rate
    while len(ADC_Value_List) < no_sample:
        current_time = time.time()
        if current_time >= start_time:
            ADC_Value = read_adc()
            ADC_Value_List.append(ADC_Value)
            start_time += interval
    return ADC_Value_List

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
        post_trigger_samples = collect_adc_data(POST_TRIGGER_TIME)
        buffer.extend(post_trigger_samples)

        # Here you can send the data over Bluetooth
        send_data_over_bluetooth(buffer)
        buffer = []
        
    # Delay to match the data rate
    time.sleep(interval)

# Close the Bluetooth sockets (this won't be reached in the current setup)
client_sock.close()
server_sock.close()
