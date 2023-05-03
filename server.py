import socket
from struct import unpack

host, port = '0.0.0.0', 65000
server_address = (host, port)

# Create a TCP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print(f'Starting TCP server on {host} port {port}')
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)

while True:
    # Wait for a connection
    connection, client_address = sock.accept()
    print(f'Connection from {client_address}')

    try:
        # Receive the data and print it
        while True:
            message = connection.recv(12)  # 3 floats * 4 bytes per float
            if not message:
                break

            print(f'Received {len(message)} bytes:')
            x, y, z = unpack('3f', message)
            print(f'X: {x}, Y: {y}, Z: {z}')

    finally:
        # Clean up the connection
        connection.close()
