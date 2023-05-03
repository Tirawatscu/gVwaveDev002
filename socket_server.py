import socket
from struct import unpack

host, port = '0.0.0.0', 65000
server_address = (host, port)

def run_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print(f'Starting TCP server on {host} port {port}')
    sock.bind(server_address)
    sock.listen(1)

    while True:
        connection, client_address = sock.accept()
        print(f'Connection from {client_address}')

        try:
            while True:
                message = connection.recv(12)
                if not message:
                    break
                print(f'Received {len(message)} bytes:')
                x, y, z = unpack('3f', message)
                print(f'X: {x}, Y: {y}, Z: {z}')

        finally:
            connection.close()
