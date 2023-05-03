from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO
import threading
import socket_server

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        num_samples = int(request.form['num_samples'])
        socket_server.set_num_samples(num_samples)
        socketio.emit('start', {'num_samples': num_samples})
        return redirect(url_for('index'))
    return render_template('index.html')

if __name__ == '__main__':
    server_thread = threading.Thread(target=socket_server.run_server)
    server_thread.start()

    socketio.run(app, debug=True, host='0.0.0.0', port=5001)
