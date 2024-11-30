import socket
import time
from datetime import datetime

LOG_FILE = f"log_udp_server-{datetime.now().strftime("%H%M%S")}.txt"

def log(message):
    with open(LOG_FILE, "a") as log_file:
        log_file.write(f"{datetime.now()} - {message}\n")
        log_file.flush()


def receive_udp(sock):
    while True:
        current_time = datetime.now().strftime("%Y-%m-%d_%H%M%S")
        data, addr = sock.recvfrom(4096)
        filename = data.decode().replace("FILENAME:", "").strip()

        with open(f"{filename}-UDP_{current_time}.bin", 'wb') as f:
            log(f"Iniciando recebimento UDP: {filename}")
            start_time = time.time()
            while True:
                data, _ = sock.recvfrom(4096)
                if data == b'FIM-CONEX4O-UDP':
                    log(f"Fim da recepção UDP para {filename}.")
                    break
                f.write(data)
            end_time = time.time()
            size = f.tell()
            log(f"Transferência UDP concluída em {end_time - start_time:.6f} segundos. Tamanho recebido: {size} bytes.")

def start_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('0.0.0.0', 12345))
    log("Servidor ouvindo UDP na porta 12345")
    receive_udp(sock)

if __name__ == "__main__":
    start_server()

