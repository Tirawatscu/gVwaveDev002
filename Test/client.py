import socket

HOST = '192.168.1.106'  # Server's IP address
PORT = 65000        # Server's port number

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(b'Hello, server!')
    data = s.recv(1024)

print(f"Received data from server: {data}")
