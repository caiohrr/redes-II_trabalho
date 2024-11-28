import socket
import time

def send_tcp(filename, sock):
    with open(filename, 'rb') as f:
        print("Enviando dados via TCP...")
        while chunk := f.read(4096):
            sock.sendall(chunk)
    # O cliente não deve fechar a conexão até o servidor ter terminado a recepção
    sock.shutdown(socket.SHUT_WR)
    sock.recv(4096)  # Espera até o servidor ter terminado a recepção

def send_udp(filename, sock, server_address):
    with open(filename, 'rb') as f:
        print("Enviando dados via UDP...")
        while chunk := f.read(4096):
            sock.sendto(chunk, server_address)
        # Envia o pacote de controle indicando o fim da conexão
        sock.sendto(b'FIM_CONEXAO_UDP', server_address)

def send_file(filename, protocol='TCP', port=12345, ip='127.0.0.1'):
    sock_type = socket.SOCK_STREAM if protocol == 'TCP' else socket.SOCK_DGRAM
    sock = socket.socket(socket.AF_INET, sock_type)

    start_time = time.time()  # Inicia a medição de tempo

    if protocol == 'TCP':
        sock.connect((ip, port))
        send_tcp(filename, sock)
    else:
        server_address = (ip, port)
        send_udp(filename, sock, server_address)

    sock.close()
    end_time = time.time()  # Finaliza a medição de tempo
    print(f"Transferência via {protocol} concluída em {end_time - start_time:.2f} segundos.")

if __name__ == '__main__':
    filename = input("Digite o nome do arquivo: ").strip()
    protocol = input("Escolha o protocolo (TCP/UDP): ").strip().upper()
    send_file(filename, protocol)

