"""
main_receiver.py  –  Main Raspberry Pi server  (best / final script)
Receives data from RpiSend, forwards it to the second server.
If the second server is unreachable → falls back to AWS IoT + CSV.
"""
import subprocess
import platform
import socket
import json
import datetime
import csv
import os
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

from config import (
    RPI_HOST, RPI_PORT,
    TARGET_HOST, TARGET_PORT,
    AWS_HOST, AWS_PORT, AWS_TOPIC,
    ROOT_CA_PATH, CERTIFICATE_PATH, PRIVATE_KEY_PATH,
    CSV_FILE_PATH,
)

# ── AWS IoT setup ──────────────────────────────────────────────────────────────
client = AWSIoTMQTTClient("MyMQTTClientID")
client.configureEndpoint(AWS_HOST, AWS_PORT)
client.configureCredentials(ROOT_CA_PATH, PRIVATE_KEY_PATH, CERTIFICATE_PATH)
client.connect()
print("Connected to AWS IoT")

# ── Helpers ────────────────────────────────────────────────────────────────────
def save_to_csv(timestamp, message):
    file_exists = os.path.isfile(CSV_FILE_PATH)
    with open(CSV_FILE_PATH, mode='a', newline='') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["timestamp", "websocket_message"])
        writer.writerow([timestamp, message])
    print(f"CSV saved: {timestamp}, {message}")

def fallback_to_aws_and_csv(payload):
    save_to_csv(payload["timestamp"], payload["websocket_message"])
    client.publish(AWS_TOPIC, json.dumps(payload), 1)
    print(f"Fallback → AWS IoT + CSV: {payload}")

def ping_host(host):
    flag = "-n" if platform.system().lower() == "windows" else "-c"
    return subprocess.call(["ping", flag, "1", host],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) == 0

def reconnect_to_target():
    try:
        s = socket.create_connection((TARGET_HOST, TARGET_PORT))
        print(f"Connected to target {TARGET_HOST}:{TARGET_PORT}")
        return s
    except socket.error as e:
        print(f"Could not reach target server: {e}")
        return None

# ── Client handler ─────────────────────────────────────────────────────────────
def handle_client(conn, addr):
    print(f"Incoming connection from {addr}")
    target = reconnect_to_target()
    try:
        while True:
            message = conn.recv(1024).decode('utf-8')
            if not message:
                break

            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            payload   = {"timestamp": timestamp, "websocket_message": message}

            if target is None or not ping_host(TARGET_HOST):
                print(f"Target unreachable – falling back")
                fallback_to_aws_and_csv(payload)
            else:
                try:
                    target.sendall(json.dumps(payload).encode('utf-8'))
                    print(f"Sent to target: {payload}")
                except socket.error as e:
                    print(f"Send error: {e} – retrying connection")
                    target.close()
                    target = reconnect_to_target()
                    if target is None:
                        fallback_to_aws_and_csv(payload)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()
        if target:
            target.close()
        print(f"Connection from {addr} closed")

# ── Main loop ──────────────────────────────────────────────────────────────────
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((RPI_HOST, RPI_PORT))
server.listen(5)
print(f"Listening on {RPI_HOST}:{RPI_PORT}")

try:
    while True:
        conn, addr = server.accept()
        handle_client(conn, addr)
except KeyboardInterrupt:
    print("Shutting down")
finally:
    client.disconnect()
    server.close()
    print("All connections closed")
