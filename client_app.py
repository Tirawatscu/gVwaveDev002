import socket
from struct import unpack, pack
import random

server_ip = '192.168.1.106'
server_port = 65000
server_address = (server_ip, server_port)

def receive_start_signal(sock):
    data = b''
    while len(data) < 8:
        data += sock.recv(8 - len(data))
    num_samples, start_signal = unpack('2i', data)
    return num_samples, start_signal


def send_samples(sock, num_samples):
    for i in range(num_samples):
        x, y, z = random.random(), random.random(), random.random()
        message = pack('3f', x, y, z)
        print(f"Sending sample {i+1}: X: {x}, Y: {y}, Z: {z}")
        sock.sendall(message)
        x += 1
        y += 1
        z += 1

def client_listen():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(server_address)

    while True:
        num_samples, start_signal = receive_start_signal(sock)
        if start_signal:
            print(f"Received start signal with {num_samples} samples")
            send_samples(sock, num_samples)
        else:
            print("No start signal received. Waiting...")

    sock.close()

if __name__ == '__main__':
    client_listen()
