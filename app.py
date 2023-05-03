from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO
import socket
from struct import unpack, pack
import random
from multiprocessing import Process

app = Flask(__name__)
socketio = SocketIO(app)

class SocketServer:
    def __init__(self, host='0.0.0.0', port=65000):
        self.host = host
        self.port = port
        self.server_address = (host, port)
        self.num_samples = 10

    def set_num_samples(self, samples):
        self.num_samples = samples

    def run_server(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print(f'Starting TCP server on {self.host} port {self.port}')
        sock.bind(self.server_address)
        sock.listen(1)

        while True:
            connection, client_address = sock.accept()
            print(f'Connection from {client_address}')

            try:
                start_signal = 1
                message = pack('1i1i', self.num_samples, start_signal)
                connection.sendall(message)

                for _ in range(self.num_samples):
                    message = connection.recv(12)
                    print(f'Received {len(message)} bytes:')
                    x, y, z = unpack('3f', message)
                    print(f'X: {x}, Y: {y}, Z: {z}')

            finally:
                connection.close()

socket_server = SocketServer()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        num_samples = int(request.form['num_samples'])
        socket_server.set_num_samples(num_samples)
        socketio.emit('start', {'num_samples': num_samples})
        return redirect(url_for('index'))
    return render_template('index.html')

if __name__ == '__main__':
    server_process = Process(target=socket_server.run_server)
    server_process.start()

    socketio.run(app, debug=True, host='0.0.0.0', port=5001, use_reloader=False)

