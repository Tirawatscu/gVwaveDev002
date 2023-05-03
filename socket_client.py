import socket
from time import sleep
import random
from struct import pack, unpack

host, port = '192.168.1.106', 65001
server_address = (host, port)

def send_samples():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(server_address)

    try:
        message = sock.recv(8)
        num_samples, start_signal = unpack('1i1i', message)

        if start_signal:
            x, y, z = random.random(), random.random(), random.random()

            for i in range(num_samples):
                message = pack('3f', x, y, z)
                sock.sendall(message)

                x += 1
                y += 1
                z += 1

    finally:
        sock.close()
