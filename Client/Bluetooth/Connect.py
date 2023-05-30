import subprocess
import select
import os
import fcntl

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

    if 'Authorize service' in output or 'Confirm passkey' in output:
        response = input('Allow device to connect? (yes/no): ')
        if response.lower() == 'yes':
            subp.stdin.write('yes\n'.encode())
            subp.stdin.flush()
        else:
            subp.stdin.write('no\n'.encode())
            subp.stdin.flush()
