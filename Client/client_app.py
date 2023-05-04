import socket
import random
import time
import select

import platform
os = platform.system()
if platform.system() == "Linux":
    import ADS1263
    import RPi.GPIO as GPIO


def generate_random_data(sample_count):
    return [round(random.uniform(0, 100), 2) for _ in range(sample_count)]

def main():
    while True:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(5)

        try:
            s.connect(('192.168.1.39', 5001))
            print("Connected to the server")
            while True:
                ready_to_read, ready_to_write, _ = select.select([s], [s], [], 1)

                if ready_to_read:
                    data = s.recv(1024)
                    if data:
                        sample_count = int(data.decode())
                        print(f"Received sample_count: {sample_count}")
                        random_data = generate_random_data(sample_count)
                        
                        if ready_to_write:
                            s.sendall(','.join(map(str, random_data)).encode())
                            print(f"Sent random data: {random_data}")
                    else:
                        break

                time.sleep(1)

        except socket.error as e:
            print(f"Connection failed. Retrying... Error: {e}")
            time.sleep(5)
        finally:
            s.close()

if __name__ == '__main__':
    main()

