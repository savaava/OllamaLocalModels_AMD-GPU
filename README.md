# 🦙 Guida Tecnica: Gestione di Ollama su Ubuntu 22.04 con GPU AMD

Questa documentazione descrive la configurazione ottimale per l'esecuzione di modelli di linguaggio locali tramite **Ollama** su una scheda video **AMD Radeon RX 6600 (8GB)**. Successivamente spiega come interfacciarsi con un client tramite ssh.

# 📋 Specifiche del Sistema
- **Sistema Operativo:** Ubuntu 22.04.5 LTS (Jammy Jellyfish)
- **GPU Dedicata:** AMD Radeon RX 6600 (Navi 23) - **Bus ID: 03:00.0**
- **GPU Integrata:** AMD Radeon Graphics - **Bus ID: 0e:00.0**
- **Driver:** `amdgpu` con supporto ROCm

# ⚙️ 1. Configurazione del Servizio (Metodo Obbligatorio)
È necessario utilizzare esclusivamente **systemctl** per la gestione del processo. L'uso diretto del comando `ollama serve` è sconsigliato in quanto ignora le configurazioni di sistema e le variabili d'ambiente ottimizzate per la GPU AMD.

**Percorso del file di override:** `/etc/systemd/system/ollama.service.d/override.conf`

## Procedura di modifica:
1. Eseguire il comando di editing del servizio:
   ```bash
   sudo systemctl edit ollama.service
   ```
2. Inserire il seguente blocco di configurazione:
   ```ini
   [Service]
   # Forza il supporto per l'architettura RDNA 2 (serie RX 6000)
   Environment="HSA_OVERRIDE_GFX_VERSION=10.3.0"
   # Disabilita il supporto per GPU Intel per evitare conflitti
   Environment="OLLAMA_INTEL_GPU=0"
   ```
3. Applicare le modifiche e riavviare il demone:
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl restart ollama
   ```

---

# 🚀 2. Gestione dei Modelli
L'interazione con i modelli deve avvenire tramite l'interfaccia a riga di comando mentre il servizio `systemctl` è in esecuzione.

| Operazione | Comando |
| :--- | :--- |
| **Avviare il servizio** | `sudo systemctl start ollama` |
| **Arrestare il servizio** | `sudo systemctl stop ollama` |
| **Elencare i modelli** | `ollama list` |
| **Scaricare un modello** | `ollama pull <nome_modello>` |
| **Eseguire un modello** | `ollama run <nome_modello>` |
| **Rimuovere un modello** | `ollama rm <nome_modello>` |

---

# 📊 3. Monitoraggio Hardware (GPU AMD)
Il monitoraggio deve essere effettuato specificamente sul **Bus 03** per verificare l'effettivo utilizzo della scheda dedicata.

## Verifica del carico (Radeontop)
L'utilizzo della GPU può essere osservato tramite il comando:
```bash
sudo radeontop -b 03
```
Si consiglia di monitorare la voce `Graphics pipe` per l'attività di calcolo e `VRAM` per l'allocazione della memoria.

## Statistiche ROCm (SMI)
Per un controllo puntuale di temperature e frequenze:
```bash
watch -n 0.5 rocm-smi
```

---

# 🛠 4. Diagnostica e FAQ

**D: Come si verifica la velocità di generazione (token al secondo)?**
R: È possibile visualizzare le statistiche prestazionali avviando il modello con il flag verbose:
```bash
ollama run llama3:8b --verbose
```
Al termine della generazione, il sistema riporterà il valore di `eval rate` espresso in token al secondo (t/s).

**D: Quali sono i log di riferimento in caso di errore?**
R: Per analizzare il comportamento del server e confermare il rilevamento della libreria ROCm, è necessario consultare i log del servizio:
```bash
journalctl -u ollama -f
```

# 🛠️ 5. Strumenti Avanzati

L'utilizzo di Ollama tramite terminale è solo il punto di partenza. Per sfruttare appieno la potenza di calcolo della GPU AMD, è opportuno integrare strumenti che trasformino il modello linguistico in un agente operativo.

### Perché utilizzare strumenti diversi?
Ogni interfaccia gestisce i **Token di Contesto** e la **VRAM** in modo differente:
- Le **WebUI** sono ideali per la conversazione generale.
- I **Sistemi RAG** servono per consultare grandi moli di dati senza saturare la memoria video.
   - Ad esempio AnythingLLM
- Gli **Agenti CLI** servono per l'interazione diretta con il file system e il codice.
   - Ad esempio Aider, Claude Code

## 📚 5.1. AnythingLLM: Il Gestore della Conoscenza (RAG)
**AnythingLLM** è la soluzione definitiva per analizzare documenti (PDF, TXT, DOCX) in locale. 
- **Efficienza VRAM:** Utilizza una tecnica di recupero (RAG) che invia alla GPU solo i frammenti di testo necessari per rispondere, permettendo di "interrogare" libri di migliaia di pagine su una scheda da 8GB.
- **Workspace Isolati:** Permette di creare aree di lavoro separate.
- **Utilizzo ideale:** Consultazione di manuali, analisi di contratti, studio di documentazione tecnica complessa.
- AnythingLLM non modifica i file, funge da lettore esperto.

## 💻 5.2. Aider: Coding Assistant
**Aider** è uno strumento da terminale che trasforma il modello (es. `qwen2.5-coder`) in un vero collaboratore capace di scrivere codice.
- **Accesso al File System:** A differenza delle chat comuni, Aider può creare nuovi file e modificare quelli esistenti direttamente nelle cartelle di progetto.
- **Integrazione Git:** Ogni modifica suggerita dall'AI può essere automaticamente seguita da un "commit", mantenendo traccia della cronologia del lavoro.
- **Utilizzo ideale:** Scrittura di script Python, creazione di siti web, automazione di task su Ubuntu, correzione di bug.

# 8. Connessione remota da un client: Tunneling SSH per Ollama col server

Questa configurazione permette di utilizzare, da un client, la GPU del server Ubuntu in sicurezza, senza esporre porte vulnerabili all'esterno.

## 8.1. Configurazione Server (Ubuntu)
Bisogna assicurarsi che il servizio sia configurato per l'ascolto locale (`localhost`)

**File:** `/etc/systemd/system/ollama.service.d/override.conf`
```ini
[Service]
Environment="HSA_OVERRIDE_GFX_VERSION=10.3.0"
Environment="OLLAMA_INTEL_GPU=0"
Environment="OLLAMA_HOST=127.0.0.1" # Per sicurezza o in generale per precisione si può inserire
```

## 8.2. Scambio di Chiavi SSH (Client → Server)
- Sul client: `ssh-keygen -t ed25519` per generare la coppia di chiavi sul client (non c'è bisogno di farlo anche sul server)
- Sul Server: inserire la chiave pubblica del client nel file `~/.ssh/authorized_keys`
  - Assicurati che i permessi sul server siano corretti, altrimenti SSH ignorerà le chiavi per sicurezza: `chmod 700 ~/.ssh && chmod 600 ~/.ssh/authorized_keys`

## 8.3. Local Forwarding: Apertura Tunnel e Gestione
Dal client, si deve eseguire questo comando per creare il ponte criptato. Ovviamente si deve mantenere questa finestra aperta durante l'uso del modello per poter mantenere la connessione.
```
ssh -L localhost:11434:localhost:11434 server_name@ip_server
```
Quindi il traffico che proviene dal client in localhost sulla porta 11434 viene inoltrato al server sulla stessa porta e quindi il traffico verrà inoltrato automaticamente alla **RX 6600** remota

## 8.4. Gestione Remota (all'interno della sessione SSH appena aperta):
Si possono eseguire i seguenti comandi dal client per gestire ollama che si trova sul server:
- `sudo systemctl start ollama`
- `sudo radeontop -b 03`
- `ollama list`
- `ollama run <nome_modello>`

## 8.5. Configurazione Software Client (AnythingLLM / Aider)
Arrivati a questo punto della configurazione del tunnel ssh, consideriamo che **Ollama URL:** `http://127.0.0.1:11434`. Quindi possiamo configurare AnythingLLM e Aider dal client:
- AnythingLLM: si seleziona Ollama come AI Provider e `http://127.0.0.1:11434` Endpoint URL.
- Aider: `aider --model ollama/qwen2.5-coder:7b --browser --openai-api-base http://127.0.0.1:11434/v1`

# 9. Utilizzo normale: procedimento completo
Assumiamo che abbiamo già installato tutto e abbiamo già condiviso la chiave pubblica con il server.
- Accendere il server e assicurarsi che sia attivo il servizio ssh, in particolare ssh lato server quindi controllare con `sudo systemctl status ssh`.
- Dal client eseguiamo `ssh -L localhost:11434:localhost:11434 server_name@ip_server` che aprirà il terminale del server tramite il tunnel cifrato di ssh
- Dal client possiamo ora eseguire `sudo systemctl start ollama`
   - Quindi ora possiamo eseguire anche `ollama list` o `ollama run <nome_modello>` per aviare il modello direttamente su terminale
   - Possiamo controllare che la connessione a Ollama del server sia avvenuta correttamente sul client andando su un browser di ricerca e digitare `localhost:11434`
- Dal client ora possiamo aprire AnythingLLM e impostare Ollama come AI Provider e `http://127.0.0.1:11434` Endpoint URL.

# 🔄 10. Tabella di Manutenzione Totale
Ecco la tabella definitiva per la manutenzione dei tutti sistemi:

| Componente | Comando di Aggiornamento | Frequenza Consigliata |
| :--- | :--- | :--- |
| **Driver/Sistema** | `sudo apt update && sudo apt upgrade` | Settimanale |
| **Ollama (Core)** | `curl -fsSL https://ollama.com/install.sh \| sh` | Mensile |
| **Aider (Coding)** | `pip install --upgrade aider-chat` | Settimanale |
| **AnythingLLM** | Riesecuzione `./installer.sh` | Al rilascio (Notifica GUI) |
| **Modelli LLM** | `ollama pull <nome_modello>` | Quando disponibili update |
| **Web Scraping** | `playwright install chromium` | Solo se Aider lo richiede |