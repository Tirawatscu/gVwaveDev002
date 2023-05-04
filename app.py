import socket
from threading import Thread
from flask import Flask, render_template, request, redirect
import time

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
    
from flask import jsonify

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
        return jsonify(received_data)


def handle_client_connection(conn, addr):
    global current_command, command_processed, received_data
    while True:
        if not command_processed:
            try:
                command_to_send = current_command
                conn.sendall(str(command_to_send).encode())
                
                # Receive data in chunks
                data = b""
                while True:
                    chunk = conn.recv(4096)
                    if not chunk:
                        break
                    data += chunk
                    if len(chunk) < 4096:
                        break
                
                received_data = list(map(float, data.decode().split(',')))
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