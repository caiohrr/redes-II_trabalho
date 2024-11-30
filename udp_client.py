import socket
import time
from datetime import datetime

LOG_FILE = f"log_udp_client-{datetime.now().strftime("%H%M%S")}.txt"

def log(message):
    with open(LOG_FILE, "a") as log_file:
        log_file.write(f"{datetime.now()} - {message}\n")

def send_udp(filename, sock, server_address):
    sock.sendto(f"FILENAME:{filename}".encode(), server_address)  # Envia o nome do arquivo
    with open(filename, 'rb') as f:
        log(f"Iniciando envio UDP: {filename}")
        while chunk := f.read(4096):
            sock.sendto(chunk, server_address)
        sock.sendto(b'FIM-CONEX4O-UDP', server_address)

def send_file(filename):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = ('127.0.0.1', 12345)  # Apontando para o servidor
    start_time = time.time()
    send_udp(filename, sock, server_address)
    end_time = time.time()
    log(f"Transferência UDP concluída em {end_time - start_time:.6f} segundos.")
    sock.close()

if __name__ == "__main__":
    files = [
        "arquivo_1MB.txt", "arquivo_10MB.txt", "arquivo_50MB.txt",
        "arquivo_125MB.txt", "arquivo_250MB.txt", "arquivo_500MB.txt",
        "arquivo_750MB.txt", "arquivo_1GB.txt", "arquivo_1.5GB.txt", "arquivo_2GB.txt"
    ]
    #files = ["arquivo_1.5GB.txt", "arquivo_2GB.txt"]
    for file in files:
        send_file(file)

