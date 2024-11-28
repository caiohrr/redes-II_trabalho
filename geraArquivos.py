import sys
import os

def generate_file(size_str):
    units = {'B': 1, 'KB': 1024, 'MB': 1024**2, 'GB': 1024**3}

    # Extrair valor numérico e unidade
    try:
        size = float(size_str[:-2])  # Pega o número
        unit = size_str[-2:].upper()  # Pega a unidade (B, KB, MB, GB)
    except ValueError:
        print("Formato inválido! Use: <número><unidade> (exemplo: 3MB, 500KB)")
        return

    if unit not in units:
        print("Unidade inválida! Escolha entre B, KB, MB ou GB.")
        return

    total_bytes = int(size * units[unit])
    filename = f"arquivo_{size_str}.txt"

    print(f"Gerando arquivo '{filename}' com {total_bytes} bytes...")

    with open(filename, 'wb') as f:
        f.write(os.urandom(total_bytes))

    print(f"Arquivo '{filename}' gerado com sucesso.")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Uso: python3 geraArquivos.py <tamanho> (exemplo: python3 geraArquivos.py 3MB)")
    else:
        generate_file(sys.argv[1])

