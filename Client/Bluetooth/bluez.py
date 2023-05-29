# This scipt use for the bluetooth transfer data to flutter application


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
                #response = str([random.random() for _ in range(100)])

                # Assuming floats_to_send is your list of floats
                floats_to_send = [1.1, 2.2, 3.3]

                # Convert the list of floats to bytes
                #response  = struct.pack('<' + 'f'*len(floats_to_send), *floats_to_send)
                response  = struct.pack('%sf' % len(floats_to_send), *floats_to_send)

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