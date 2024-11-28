import socket
import time

def send_tcp(filename, sock):
    with open(filename, 'rb') as f:
        print("Enviando dados via TCP...")
        while chunk := f.read(4096):
            sock.sendall(chunk)
    sock.shutdown(socket.SHUT_WR)

def send_udp(filename, sock, server_address):
    with open(filename, 'rb') as f:
        print("Enviando dados via UDP...")
        while chunk := f.read(4096):
            sock.sendto(chunk, server_address)

def send_file(filename, protocol='TCP', port=12345, ip='127.0.0.1'):
    sock_type = socket.SOCK_STREAM if protocol == 'TCP' else socket.SOCK_DGRAM
    sock = socket.socket(socket.AF_INET, sock_type)

    if protocol == 'TCP':
        sock.connect((ip, port))
        send_tcp(filename, sock)
    else:
        server_address = (ip, port)
        send_udp(filename, sock, server_address)

    sock.close()
    print(f"Transferência via {protocol} concluída.")

if __name__ == '__main__':
    filename = input("Digite o nome do arquivo: ").strip()
    protocol = input("Escolha o protocolo (TCP/UDP): ").strip().upper()
    send_file(filename, protocol, ip='10.254.225.14')

