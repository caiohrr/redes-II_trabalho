import socket
import time
from datetime import datetime

def receive_tcp(sock):
    conn, _ = sock.accept()
    with conn:
        current_time = datetime.now().strftime("%Y-%m-%d_%H%M%S")
        with open(f"received_tcp.{current_time}", 'wb') as f:
            print("Recebendo dados via TCP...")
            start_time = time.time()  # Inicia a medição de tempo após o servidor começar a receber dados
            while True:
                data = conn.recv(4096)
                if not data:
                    break
                f.write(data)
            end_time = time.time()  # Finaliza a medição de tempo após a recepção de todos os dados
            print(f"Transferência via TCP concluída em {end_time - start_time:.2f} segundos.")

def receive_udp(sock):
    current_time = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    with open(f"received_udp.{current_time}", 'wb') as f:
        print("Recebendo dados via UDP...")
        start_time = time.time()  # Inicia a medição de tempo após o servidor começar a receber dados
        while True:
            try:
                sock.settimeout(1000)  # Timeout para encerrar a recepção
                data, _ = sock.recvfrom(4096)
                if data == b'FIM_CONEXAO_UDP':  # Pacote de controle que indica o fim
                    print("Fim da recepção UDP.")
                    break
                if not data:
                    break
                f.write(data)
            except socket.timeout:
                print("Fim da recepção UDP por timeout.")
                break
        end_time = time.time()  # Finaliza a medição de tempo após a recepção de todos os dados
        print(f"Transferência via UDP concluída em {end_time - start_time:.2f} segundos.")

def start_server(protocol='TCP', port=12345):
    sock_type = socket.SOCK_STREAM if protocol == 'TCP' else socket.SOCK_DGRAM
    sock = socket.socket(socket.AF_INET, sock_type)
    sock.bind(('0.0.0.0', port))

    if protocol == 'TCP':
        sock.listen(1)
        receive_tcp(sock)
    else:
        receive_udp(sock)

    sock.close()

if __name__ == '__main__':
    protocol = input("Escolha o protocolo (TCP/UDP): ").strip().upper()
    start_server(protocol)

