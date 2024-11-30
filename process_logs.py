import re
import csv
import os

# Atualização da regex para capturar tamanhos com decimais (ex: 1.5GB, 1MB)
SERVER_LOG_PATTERN = r"Iniciando recebimento (\w+): .*?arquivo_([\d.]+[MG]B).*?\n.*?Transferência \1 concluída em ([0-9.]+) segundos. Tamanho recebido: (\d+) bytes."

CSV_FILE = "transferencias_servidor.csv"

def parse_log(file_path):
    """Parse a server log file and return data as a list of dictionaries."""
    results = []
    with open(file_path, "r") as file:
        content = file.read()
        matches = re.findall(SERVER_LOG_PATTERN, content, re.MULTILINE | re.DOTALL)

        for match in matches:
            protocol, size, duration, bytes_received = match
            results.append({
                "protocol": protocol,
                "size": size,
                "duration": float(duration),
                "size_bytes": int(bytes_received)
            })
    return results

def write_csv(data):
    """Write parsed data to CSV file, appending if the file already exists."""
    file_exists = os.path.isfile(CSV_FILE)
    with open(CSV_FILE, mode="a", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["protocol", "size", "duration", "size_bytes"])
        if not file_exists:
            writer.writeheader()
        writer.writerows(data)

def find_server_logs():
    """Find all server log files in the current directory."""
    return [file for file in os.listdir() if "server" in file and file.endswith(".txt")]

def process_logs():
    """Process all server logs and generate a consolidated CSV."""
    all_data = []
    log_files = find_server_logs()

    for file in log_files:
        parsed_data = parse_log(file)
        all_data.extend(parsed_data)
    
    write_csv(all_data)

if __name__ == "__main__":
    process_logs()
    print(f"Resultados salvos no arquivo '{CSV_FILE}'.")

