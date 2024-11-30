import socket
import time
from datetime import datetime

LOG_FILE = f"log_tcp_server-{datetime.now().strftime("%H%M%S")}.txt"

def log(message):
    with open(LOG_FILE, "a") as log_file:
        log_file.write(f"{datetime.now()} - {message}\n")
        log_file.flush()

def receive_tcp(sock):
    conn, _ = sock.accept()
    with conn:
        filename = conn.recv(1024).decode()  # Receive the filename from the client
        timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
        save_filename = f"{filename}-TCP_{timestamp}.bin"
        
        log(f"Iniciando recebimento TCP: {save_filename}")
        
        with open(save_filename, 'wb') as f:
            start_time = time.time()
            total_bytes = 0
            while True:
                data = conn.recv(4096)
                if not data:
                    break
                f.write(data)
                total_bytes += len(data)
            end_time = time.time()
        
        log(f"Transferência TCP concluída em {end_time - start_time:.6f} segundos. Tamanho recebido: {total_bytes} bytes.")

def start_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('0.0.0.0', 12345))
    sock.listen(1)
    log("Servidor ouvindo TCP na porta 12345")

    while True:
        receive_tcp(sock)

if __name__ == "__main__":
    start_server()
