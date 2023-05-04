import socket
import random
import time
import select

import platform
os = platform.system()
if platform.system() == "Linux":
    import ADS1263
    import RPi.GPIO as GPIO

REF = 5.08          # Modify according to actual voltage
                    # external AVDD and AVSS(Default), or internal 2.5V
                    
ADC = ADS1263.ADS1263()
if (ADC.ADS1263_init_ADC1('ADS1263_4800SPS') == -1):
    ADC.ADS1263_Exit()
    print("Failed to initialize ADC1")
    exit()
ADC.ADS1263_SetMode(1)
sampling_rate = 128  # Hz
sleep_duration = 1 / sampling_rate

def generate_random_data(sample_count):
    return [round(random.uniform(0, 100), 2) for _ in range(sample_count)]

def collect_adc_data(duration):
    global ADC
    channelList = [0]
    start_time = time.perf_counter()
    ADC_Value_List = []

    sampling_rate = 128  # Hz
    interval = 1 / sampling_rate
    next_sample_time = start_time + interval
    no_sample = duration * sampling_rate
    
    current_time = start_time  # Initialize current_time variable here
    
    while len(ADC_Value_List) < no_sample:
        current_time = time.perf_counter()
        if current_time >= next_sample_time:
            ADC_Value = ADC.ADS1263_GetAll(channelList)
            ADC_Value_List.append(ADC_Value)
            next_sample_time = current_time + interval

    actual_sampling_rate = len(ADC_Value_List) / (current_time - start_time)
    
    converted_data = {channel: [] for channel in channelList}
    for data in ADC_Value_List:
        for channel, value in enumerate(data):
            if value >> 31 == 1:
                converted_data[channel].append(-(REF * 2 - value * REF / 0x80000000))
            else:
                converted_data[channel].append(value * REF / 0x7fffffff)
    return converted_data, actual_sampling_rate


def main():
    while True:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(5)

        try:
            s.connect(('192.168.1.39', 5001))
            print("Connected to the server")
            while True:
                ready_to_read, ready_to_write, _ = select.select([s], [s], [], 1)

                if ready_to_read:
                    data = s.recv(1024)
                    if data:
                        sample_count = int(data.decode())
                        print(f"Received sample_count: {sample_count}")
                        duration = int(sample_count/sampling_rate)
                        random_data, actual_sampling_rate = collect_adc_data(duration)
                        print(actual_sampling_rate)
                        
                        if ready_to_write:
                            s.sendall(','.join(map(str, random_data)).encode())
                            print(f"Sent random data: {random_data}")
                    else:
                        break

                time.sleep(1)

        except socket.error as e:
            print(f"Connection failed. Retrying... Error: {e}")
            time.sleep(5)
        finally:
            s.close()

if __name__ == '__main__':
    main()

