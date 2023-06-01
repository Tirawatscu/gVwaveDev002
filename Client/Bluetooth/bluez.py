# This scipt use for the bluetooth transfer data to flutter application
#bluez.py

import bluetooth
import random
import struct
import time

def send_data(sock, data):
    total_sent = 0
    while total_sent < len(data):
        sent = sock.send(data[total_sent:])
        if sent == 0:
            raise RuntimeError("socket connection broken")
        total_sent = total_sent + sent
        print(total_sent)

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
            #print("Received: [%s]" % data)

            # Send a response
            data_str = data.decode("utf-8").strip()
            if data_str == "Start":

                # Generate 2000 random floats between -1 and 1
                floats_to_send = [round(random.uniform(-1, 1), 5) for _ in range(250)]
                # Convert each float to string and join them into a single string
                string_data = 'START\n' + ','.join(map(str, floats_to_send)) + '\nEND'

                # Convert the string to bytes
                byte_data = string_data.encode('utf-8')

                # Chunk size
                chunk_size = 512  # You can adjust this value

                # Send the byte data in chunks
                for i in range(0, len(byte_data), chunk_size):
                    send_data(client_sock, byte_data[i:i+chunk_size])
                    time.sleep(0.1)
                print(floats_to_send)
                print('complete')    

                # At this point, bytes_to_send can be sent using a BLE library in Python
            else:
                response = "No Response"

        except Exception as e:
            print(f"An error occurred: {e}")
            client_sock, address = server_sock.accept()
            print("Accepted connection from", address)

    client_sock.close()  # this won't be reached in the current setup
    server_sock.close()

listen_for_connections()