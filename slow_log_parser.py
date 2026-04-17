import re

LOG_PATTERN = r'(?P<ip>\S+) \S+ \S+ \[(?P<date>.*?)\] "(?P<method>\S+) (?P<url>\S+) \S+" (?P<status>\d+) (?P<size>\d+)'

def analyze_logs(path):
    # ERRORE 1: Carica l'intero file in memoria. 
    # Se il file è > 1GB e hai 8GB di RAM, il sistema userà lo SWAP e diventerà lentissimo.
    with open(path, 'r') as f:
        lines = f.readlines() 

    results = []
    
    # ERRORE 2: Elaborazione sequenziale (usa un solo core della CPU).
    for line in lines:
        match = re.search(LOG_PATTERN, line)
        if match:
            # ERRORE 3: Creazione di una lista enorme di oggetti in memoria.
            results.append(match.groupdict())

    # ERRORE 4: Ciclo aggiuntivo per il conteggio (inefficiente).
    count_200 = 0
    for entry in results:
        if entry['status'] == '200':
            count_200 += 1
            
    print(f"Analisi completata. Richieste 200 OK: {count_200}")

if __name__ == "__main__":
    # Assicurati che il file esista prima di testare
    LOG_FILE = "/var/log/apache2/access.log"
    analyze_logs(LOG_FILE)