from mqtt_as import MQTTClient, config
import uasyncio as asyncio
from machine import Pin
import dht
import time
from MMA8452Q import MMA8452Q
import network

# Initialize the DHT sensor.
sensor = dht.DHT11(Pin(13))

# Dictionary of Wi-Fi SSIDs and their corresponding passwords
wifi_networks = {'Tiraway_2.4G': 'ball130737', 'BBWIFI': '0896629590', 'Geoverse_Super_WIFI': '17377331', 'GeoverseWIFI': '98747801'}

# Local configuration
config['user'] = 'gvdevmqtt'
config['password'] = 'Geoverse@5'
broker = '1b31e8cbcd6d4d46aa695d71251f143c.s2.eu.hivemq.cloud'
config['server'] = broker
config['ssl'] = True
config['ssl_params'] = {"server_hostname": broker}

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


mma8452q = MMA8452Q()

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
        accl = mma8452q.read_accl()
        temp = sensor.temperature()  # Fetch temperature.
        hum = sensor.humidity()  # Fetch humidity.
        '''print('Temperature: %3.1f C' %temp)
        print('Humidity: %3.1f %%' %hum)
        print("Acceleration in X-Axis : %.3f" %(accl['x']))
        print("Acceleration in Y-Axis : %.3f" %(accl['y']))
        print("Acceleration in Z-Axis : %.3f" %(accl['z']))
        print("*************************************")'''
        print('publish')
        # If WiFi is down the following will pause for the duration.
        await client.publish('Temperature/gv01', '{}'.format(temp), qos = 1)
        await client.publish('Humidity/gv01', '{}'.format(hum), qos = 1)
        await client.publish('Accl/gv01', '{},{},{}'.format(accl['x'], accl['y'], accl['z']), qos = 1)
        await asyncio.sleep(5)


config["queue_len"] = 1  # Use event interface with default queue size
MQTTClient.DEBUG = True  # Optional: print diagnostic messages
client = MQTTClient(config)
try:
    asyncio.run(main(client))
finally:
    client.close()  # Prevent LmacRxBlk:1 errors
