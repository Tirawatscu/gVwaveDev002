'''import network
import time

def connect_wifi(ssid, password):
    station = network.WLAN(network.STA_IF)
    station.active(True)
    station.connect(ssid, password)
    
    # check for the connection status
    while station.isconnected() == False:
        pass

    print('Connection successful')
    print(station.ifconfig())

# provide your wifi credentials here
ssid = "TSK"
password = "11110000"

connect_wifi(ssid, password)'''
