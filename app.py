from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO
import socket_server
from multiprocessing import Process

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
    server_process = Process(target=socket_server.run_server)
    server_process.start()

    socketio.run(app, debug=True, host='0.0.0.0', port=5001)
