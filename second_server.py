"""
second_server.py  –  Second / target server
Listens for JSON data forwarded by main_receiver.py.
Run this on the machine at TARGET_HOST (192.168.2.100).
"""
import socket
from config import TARGET_HOST, TARGET_PORT

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((TARGET_HOST, TARGET_PORT))
    server.listen(1)
    print(f"Listening on {TARGET_HOST}:{TARGET_PORT} ...")

    conn, addr = server.accept()
    with conn:
        print(f"Connected by {addr}")
        while True:
            data = conn.recv(1024)
            if not data:
                break
            print("Received:", data.decode("utf-8"))
        print("Connection closed.")
