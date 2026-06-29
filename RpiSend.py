"""
RpiSend.py  –  Sensor / client side
Connects to the Raspberry Pi server and sends timestamped data every 5 seconds.
"""
import time
import datetime
import random
import socket
from config import RPI_HOST, RPI_PORT

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    client_socket.connect((RPI_HOST, RPI_PORT))
    print(f"Connected to {RPI_HOST}:{RPI_PORT}")
except Exception as e:
    print(f"Could not connect to {RPI_HOST}:{RPI_PORT}. Error: {e}")
    exit(1)

try:
    while True:
        timestamp     = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        random_number = random.randint(1, 500)
        message       = f"{timestamp}: Hello, Server! - Random Number: {random_number}"

        client_socket.sendall(message.encode())
        print(f"Sent: {message}")
        time.sleep(5)

except KeyboardInterrupt:
    print("Script interrupted by user")
finally:
    client_socket.close()
    print("Connection closed")
