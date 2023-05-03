from flask import Flask, render_template
from flask_socketio import SocketIO
import socket_client

app = Flask(__name__)
socketio = SocketIO(app)

@socketio.on('connect')
def handle_connect():
    print("WebSocket connected")
    
@socketio.on('start')
def handle_start(data):
    num_samples = data['num_samples']
    print(f"Received start signal with {num_samples} samples")
    socket_client.send_samples(num_samples)


if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=5001)
