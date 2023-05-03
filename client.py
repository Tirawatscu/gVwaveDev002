import socket
from time import sleep
import random
from struct import pack, unpack

host, port = '192.168.1.106', 65000
server_address = (host, port)

# Create a TCP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
sock.connect(server_address)

try:
    # Wait for the command from the server
    message = sock.recv(8)  # 2 integers * 4 bytes per integer
    num_samples, start_signal = unpack('1i1i', message)

    if start_signal:
        # Generate some random start values
        x, y, z = random.random(), random.random(), random.random()

        # Send the specified number of samples
        for i in range(num_samples):
            # Pack three 32-bit floats into message and send
            message = pack('3f', x, y, z)
            sock.sendall(message)
            sleep(1/128)
            x += 1
            y += 1
            z += 1

finally:
    # Close the connection
    sock.close()
