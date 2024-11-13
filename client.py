# echo-client.py

import socket

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65432  # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    while True:
        msg = input("Message to send to server: ")
        s.sendall(bytes(msg, encoding='utf-8'))
        print(f"sent {msg}")
        data = s.recv(1024)
        print(f"Received {data!r}")
