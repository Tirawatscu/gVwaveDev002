import socket
import random
from struct import pack

server_ip = '192.168.1.106'  # Replace with the server's IP address

host, port = server_ip, 65000
server_address = (host, port)

def send_samples(num_samples):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(server_address)
    print("Connected")

    try:
        x, y, z = random.random(), random.random(), random.random()

        for i in range(num_samples):
            message = pack('3f', x, y, z)
            sock.sendall(message)

            x += 1
            y += 1
            z += 1

    finally:
        sock.close()
