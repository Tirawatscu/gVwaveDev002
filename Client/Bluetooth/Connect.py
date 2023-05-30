import subprocess
import select
import os
import fcntl
import time

# Open a subprocess with bluetoothctl
subp = subprocess.Popen(
    ['bluetoothctl'], 
    stdin=subprocess.PIPE, 
    stdout=subprocess.PIPE, 
    stderr=subprocess.PIPE)

# Set the O_NONBLOCK flag of subp.stdout file descriptor:
flags = fcntl.fcntl(subp.stdout, fcntl.F_GETFL)  # get current subp.stdout flags
fcntl.fcntl(subp.stdout, fcntl.F_SETFL, flags | os.O_NONBLOCK)

# Commands to run initially
initial_commands = [
    'power on',
    'agent on',
    'default-agent',
    'discoverable on',
    'pairable on',
]

# Send initial commands
for command in initial_commands:
    subp.stdin.write((command + '\n').encode())
    subp.stdin.flush()

while True:
    # Wait for data to be available on subp.stdout
    select.select([subp.stdout], [], [])

    output = subp.stdout.readline().decode()
    print(output.strip())

    # If there's an incoming pairing request, automatically accept it
    if 'Request confirmation' in output: 
        # Wait for a moment to ensure the input is correctly received
        time.sleep(1)
        subp.stdin.write('yes\n'.encode())
        subp.stdin.flush()
