# This scipt use for the bluetooth transfer data to flutter application
#bluez.py

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
            #print("Received: [%s]" % data)

            # Send a response
            data_str = data.decode("utf-8").strip()
            if data_str == "Start":
                floats_to_send = [1.1, 2.2, 3.3]

                # Convert the list of floats to a space-separated string
                floats_str = ' '.join(map(str, floats_to_send))
                
                # Encode this string to bytes
                bytes_str = floats_str.encode()

                # Convert bytes to integers for Uint8List
                uint8_list = [int(b) for b in bytes_str]
                
                # Now pack this uint8 list to bytes
                response = bytes(uint8_list)

                # At this point, bytes_to_send can be sent using a BLE library in Python
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

listen_for_connections()