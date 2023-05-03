import socket
from struct import unpack, pack
import socket_client

host, port = '0.0.0.0', 65001
server_address = (host, port)

num_samples = 10

def set_num_samples(samples):
    global num_samples
    num_samples = samples

def run_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print(f'Starting TCP server on {host} port {port}')
    sock.bind(server_address)
    sock.listen(1)

    while True:
        connection, client_address = sock.accept()
        print(f'Connection from {client_address}')

        try:
            start_signal = 1
            message = pack('1i1i', num_samples, start_signal)
            connection.sendall(message)

            for _ in range(num_samples):
                message = connection.recv(12)
                print(f'Received {len(message)} bytes:')
                x, y, z = unpack('3f', message)
                print(f'X: {x}, Y: {y}, Z: {z}')

        finally:
            connection.close()

