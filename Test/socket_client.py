import socket
import random
from struct import pack
import struct

server_ip = '192.168.1.36'  # Replace with the server's IP address

host, port = server_ip, 5001
server_address = (host, port)

def send_samples(num_samples):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(server_address)

    try:
        while True:
            x, y, z = random.random(), random.random(), random.random()
            message = struct.pack('3f', x, y, z)
            print(f"Sending sample {i+1}: X: {x}, Y: {y}, Z: {z}")
            sock.sendall(message)

            data = sock.recv(8)
            if data == b'stop':
                break

    finally:
        sock.close()