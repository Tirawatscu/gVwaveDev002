#Server
import socket
from threading import Thread
from flask import Flask, render_template, request, redirect
import time
import json
from flask import jsonify

app = Flask(__name__)

current_command = 0
command_processed = True

@app.route('/', methods=['GET', 'POST'])
def index():
    global current_command, command_processed
    if request.method == 'POST':
        current_command = int(request.form['command'])
        command_processed = False
        return redirect('/')
    else:
        return render_template('index.html')
    
# Add a new global variable to store the received data
received_data = []

@app.route('/get_data', methods=['POST'])
def get_data():
    global current_command, command_processed, received_data
    if request.method == 'POST':
        current_command = int(request.form['command'])
        command_processed = False
        # Wait until the command is processed
        while not command_processed:
            time.sleep(0.1)

        # Convert the data to a format suitable for plotting
        plot_data = []
        for channel, values in received_data.items():
            for i, value in enumerate(values):
                plot_data.append({'channel': int(channel), 'sample': i, 'value': value})

        return jsonify(plot_data)


def handle_client_connection(conn, addr):
    global current_command, command_processed, received_data
    while True:
        if not command_processed:
            try:
                command_to_send = current_command
                conn.sendall(str(command_to_send).encode())

                # Receive the length of the data
                data_length = int(conn.recv(8).decode())

                # Receive data in chunks
                data = b""
                remaining_data = data_length
                while remaining_data > 0:
                    chunk = conn.recv(min(remaining_data, 4096))
                    if not chunk:
                        break
                    data += chunk
                    remaining_data -= len(chunk)
                
                received_data = json.loads(data.decode())  # Deserialize JSON data
                print(f"Received random data: {received_data}")
                command_processed = True
            except Exception as e:
                print(f"Error in handle_client_connection: {e}")
                break
    conn.close()

def start_server(port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', port))
    server.listen(5)

    print(f"Listening on port {port}")

    while True:
        conn, addr = server.accept()
        print(f"Connected on port {port} by {addr}")
        Thread(target=handle_client_connection, args=(conn, addr)).start()

if __name__ == '__main__':
    Thread(target=start_server, args=(5001,)).start()
    app.run(host='0.0.0.0', port=8080)