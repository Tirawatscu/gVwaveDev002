from mqtt_as import MQTTClient, config
import uasyncio as asyncio
from machine import Pin
import dht
import time
#from MMA8452Q import MMA8452Q
import network

# Initialize the DHT sensor.
sensor = dht.DHT11(Pin(13))

# Dictionary of Wi-Fi SSIDs and their corresponding passwords
wifi_networks = {'Tiraway_2.4G': 'ball130737', 'BBWIFI': '0896629590', 'Geoverse_Super_WIFI': '17377331', 'GeoverseWIFI': '98747801', 'TSK': '11110000'}

# Local configuration
ACCESS_TOKEN = "0te3rhgymg0f7ta0qlv6"  # Replace with your actual access token
config['user'] = ACCESS_TOKEN
config['password'] = ''
broker = 'geoversedev.trueddns.com'
config['server'] = broker
config['port'] = 40694
#config['ssl'] = True
#config['ssl_params'] = {"server_hostname": broker}
#config['ssl_params'] = {"key": ACCESS_TOKEN}


# Connect to Wi-Fi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)

# Scan for available networks
print('Scanning for networks...')
networks = wlan.scan()

# Filter for networks in the list of SSIDs
available_networks = [network for network in networks if network[0].decode('utf-8') in wifi_networks.keys()]

if not available_networks:
    print('No known networks found')
else:
    # Sort networks by signal strength (index 3)
    available_networks.sort(key=lambda x: x[3], reverse=True)

    # Connect to the network with the strongest signal
    strongest_network = available_networks[0][0].decode('utf-8')
    wifi_password = wifi_networks[strongest_network]
    print('Connecting to', strongest_network)
    #wlan.connect(strongest_network, wifi_password)

    # Wait for the connection to complete
    #while not wlan.isconnected():
    #    time.sleep(1)

    print('Connected to', strongest_network)
    config['ssid'] = strongest_network
    config['wifi_pw'] = wifi_password


#mma8452q = MMA8452Q()

async def messages(client):  # Respond to incoming messages
    async for topic, msg, retained in client.queue:
        print((topic, msg, retained))

async def up(client):  # Respond to connectivity being (re)established
    while True:
        await client.up.wait()  # Wait on an Event
        client.up.clear()
        await client.subscribe('foo_topic', 1)  # renew subscriptions

async def main(client):
    await client.connect()
    for coroutine in (up, messages):
        asyncio.create_task(coroutine(client))
    while True:
        sensor.measure()
        #accl = mma8452q.read_accl()
        temp = sensor.temperature()  # Fetch temperature.
        hum = sensor.humidity()  # Fetch humidity.
        '''payload = {
            "temperature": temp,
            "humidity": hum,
            "acceleration_x": accl['x'],
            "acceleration_y": accl['y'],
            "acceleration_z": accl['z'],
        }'''
        payload = {
            "temperature": temp,
            "humidity": hum,
            }
        print('publish', payload)
        # If WiFi is down the following will pause for the duration.
        await client.publish('v1/devices/me/telemetry', '{}'.format(payload), qos = 0)
        await asyncio.sleep(5)
        #time.sleep(5)


config["queue_len"] = 5  # Use event interface with default queue size
MQTTClient.DEBUG = True  # Optional: print diagnostic messages
client = MQTTClient(config)
try:
    asyncio.run(main(client))
finally:
    client.close()  # Prevent LmacRxBlk:1 errors
