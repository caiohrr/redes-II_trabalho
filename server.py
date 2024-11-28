import socket
import time
from datetime import datetime

def receive_tcp(sock):
    conn, _ = sock.accept()
    with conn:
        with open(f"received_tcp.dat{datetime.now().strftime("%Y-%m-%d_%H%M%S")}", 'wb') as f:
            print("Recebendo dados via TCP...")
            while True:
                data = conn.recv(4096)
                if not data:
                    break
                f.write(data)

def receive_udp(sock):
    with open(f"received_udp.{datetime.now().strftime("%Y-%m-%d_%H%M%S")}", 'wb') as f:
        print("Recebendo dados via UDP...")
        while True:
            try:
                sock.settimeout(10)  # Timeout para encerrar a recepção
                data, _ = sock.recvfrom(4096)
                if not data:
                    break
                f.write(data)
            except socket.timeout:
                print("Fim da recepção UDP por timeout.")
                break

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
    print(f"Transferência via {protocol} concluída.")

if __name__ == '__main__':
    protocol = input("Escolha o protocolo (TCP/UDP): ").strip().upper()
    start_server(protocol)

