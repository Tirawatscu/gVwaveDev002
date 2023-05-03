import socket
from struct import unpack, pack
import random

server_ip = '192.168.1.106'  # Replace with the server's IP address
host, port = server_ip, 65000
server_address = (host, port)


def receive_start_signal(sock):
    data = b''
    while len(data) < 8:
        data += sock.recv(8 - len(data))
    num_samples, start_signal = unpack('2i', data)
    return num_samples, start_signal


def send_samples(sock, num_samples):
    x, y, z = random.random(), random.random(), random.random()

    for i in range(num_samples):
        message = pack('3f', x, y, z)
        print(f"Sending sample {i + 1}: X: {x}, Y: {y}, Z: {z}")
        sock.sendall(message)

        x += 1
        y += 1
        z += 1


def client_listen():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(server_address)

    try:
        num_samples, start_signal = receive_start_signal(sock)
        if start_signal == 1:
            print(f"Received start signal with {num_samples} samples")
            send_samples(sock, num_samples)
    finally:
        sock.close()


if __name__ == "__main__":
    client_listen()
