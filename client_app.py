from flask import Flask, render_template
from flask_socketio import SocketIO
import socket_client

app = Flask(__name__)
socketio = SocketIO(app, async_mode='threading')

@socketio.on('connect')
def on_connect():
    print("WebSocket connected")
    # Rest of your code

@socketio.on('start_signal_response')
def on_start_signal_response(data):
    print(f"Received response from server: {data}")

    
@socketio.on('start')
def handle_start(data):
    num_samples = data['num_samples']
    print(f"Received start signal with {num_samples} samples")
    socket_client.send_samples(num_samples)


if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=5001)
