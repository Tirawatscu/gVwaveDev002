import socketio

sio = socketio.Client()

@sio.event
def connect():
    print("I'm connected!")
    sio.emit('client_message', {'data': 'Hello, server!'})

@sio.event
def disconnect():
    print("I'm disconnected!")

@sio.on('server_message')
def on_message(data):
    print('Received message:', data)
    send(data)
    
@sio.event
def send(data):
    sio.emit('client_message', {'data': f'{data} Again'})
    

sio.connect('http://192.168.1.103:5000')
sio.wait()
