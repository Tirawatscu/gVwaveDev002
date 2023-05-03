from flask import Flask, render_template, request, redirect, url_for
import threading
import socket_server

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        num_samples = int(request.form['num_samples'])
        socket_server.set_num_samples(num_samples)
        socket_server.start_client()
        return redirect(url_for('index'))
    return render_template('index.html')

if __name__ == '__main__':
    server_thread = threading.Thread(target=socket_server.run_server)
    server_thread.start()

    app.run(debug=True, host="0.0.0.0", port=5200)
