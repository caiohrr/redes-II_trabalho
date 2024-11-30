import socket
import time
from datetime import datetime

LOG_FILE = f"log_tcp_client-{datetime.now().strftime('%H%M%S')}.txt"

def log(message):
    with open(LOG_FILE, "a") as log_file:
        log_file.write(f"{datetime.now()} - {message}\n")
        log_file.flush()

def send_tcp(filename, sock):
    sock.sendall(filename.encode())  # Send the filename to the server
    time.sleep(0.1)  # Small delay to ensure the filename is processed first
    
    with open(filename, 'rb') as f:
        log(f"Iniciando envio TCP: {filename}")
        while chunk := f.read(4096):
            sock.sendall(chunk)

def send_file(filename):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('10.254.225.12', 12345))  # Connect to the server
    start_time = time.time()
    
    send_tcp(filename, sock)
    
    sock.shutdown(socket.SHUT_WR)  # Close the sending side of the socket
    
    # Wait for the server to close the connection cleanly
    try:
        sock.recv(1024)
    except ConnectionResetError:
        pass
    
    sock.close()
    
    end_time = time.time()
    log(f"Transferência TCP concluída em {end_time - start_time:.6f} segundos.")

if __name__ == "__main__":
    files = [
        "arquivo_1MB.txt", "arquivo_10MB.txt", "arquivo_50MB.txt",
        "arquivo_125MB.txt", "arquivo_250MB.txt", "arquivo_500MB.txt",
        #"arquivo_750MB.txt", "arquivo_1GB.txt", "arquivo_1.5GB.txt", "arquivo_2GB.txt"
    ]
    for file in files:
        send_file(file)

