import socket
import sys
from time import sleep
import random
from struct import pack

host, port = '192.168.1.106', 65000
server_address = (host, port)

# Create a TCP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
sock.connect(server_address)

# Generate some random start values
x, y, z = random.random(), random.random(), random.random()

# Send a few messages
for i in range(2048):
    # Pack three 32-bit floats into message and send
    message = pack('3f', x, y, z)
    sock.sendall(message)

    sleep(1/128)
    x += 1
    y += 1
    z += 1

# Close the connection
sock.close()
