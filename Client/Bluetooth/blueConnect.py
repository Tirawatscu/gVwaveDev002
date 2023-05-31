import subprocess
import select
import os
import fcntl
import time
import bluetooth
import random
import struct

def listen_for_connections():
    server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

    port = 1
    server_sock.bind(("", port))
    server_sock.listen(1)

    print("Listening for connections on RFCOMM channel", port)

    client_sock, address = server_sock.accept()
    print("Accepted connection from", address)

    while True:
        try:
            data = client_sock.recv(1024)

            # Send a response
            data_str = data.decode("utf-8").strip()
            if data_str == "Start":
                floats_to_send = [1.1, 2.2, 3.3]
                response  = struct.pack('%sf' % len(floats_to_send), *floats_to_send)
            else:
                response = "No Response"
            
            print("Received: [%s]" % data_str)
            client_sock.send(response)
            print("Sent response:", response)
        except Exception as e:
            print(f"An error occurred: {e}")
            client_sock, address = server_sock.accept()
            print("Accepted connection from", address)

    client_sock.close()  # this won't be reached in the current setup
    server_sock.close()
    

# Check for existing connections
def check_existing_connections():
    result = subprocess.run(['bluetoothctl', 'info'], stdout=subprocess.PIPE)
    lines = result.stdout.decode('utf-8').splitlines()
    for line in lines:
        if 'Connected: yes' in line:
            return True
    return False

if not check_existing_connections():
    # Open a subprocess with bluetoothctl
    subp = subprocess.Popen(
        ['bluetoothctl'], 
        stdin=subprocess.PIPE, 
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE)

    # Set the O_NONBLOCK flag of subp.stdout file descriptor:
    flags = fcntl.fcntl(subp.stdout, fcntl.F_GETFL)  # get current subp.stdout flags
    fcntl.fcntl(subp.stdout, fcntl.F_SETFL, flags | os.O_NONBLOCK)

    # Commands to run initially
    initial_commands = [
        'power on',
        'agent on',
        'default-agent',
        'discoverable on',
        'pairable on',
    ]

    # Send initial commands
    for command in initial_commands:
        time.sleep(1)
        subp.stdin.write((command + '\n').encode())
        subp.stdin.flush()

    while True:
        # Wait for data to be available on subp.stdout
        select.select([subp.stdout], [], [])

        output = subp.stdout.readline().decode()
        print(output.strip())

        # If there's an incoming pairing request or a service authorization request, automatically accept it
        if 'Request confirmation' in output or 'Authorize service' in output:
            # Wait for a moment to ensure the input is correctly received
            time.sleep(2)
            subp.stdin.write('yes\n'.encode())
            subp.stdin.flush()

        if 'Paired: yes' in output:
            break

    subp.terminate()

listen_for_connections()

