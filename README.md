# 🦙 Guida Tecnica: Gestione di Ollama su Ubuntu 22.04 con GPU AMD

Questa documentazione descrive la configurazione ottimale per l'esecuzione di modelli di linguaggio locali tramite **Ollama** su una scheda video **AMD Radeon RX 6600 (8GB)**. Il sistema è configurato per gestire correttamente la doppia GPU (Integrata + Dedicata).

---

## 📋 Specifiche del Sistema
- **Sistema Operativo:** Ubuntu 22.04.5 LTS (Jammy Jellyfish)
- **GPU Dedicata:** AMD Radeon RX 6600 (Navi 23) - **Bus ID: 03:00.0**
- **GPU Integrata:** AMD Radeon Graphics - **Bus ID: 0e:00.0**
- **Driver:** `amdgpu` con supporto ROCm

---

## ⚙️ 1. Configurazione del Servizio (Metodo Obbligatorio)
È necessario utilizzare esclusivamente **systemctl** per la gestione del processo. L'uso diretto del comando `ollama serve` è sconsigliato in quanto ignora le configurazioni di sistema e le variabili d'ambiente ottimizzate per la GPU AMD.

**Percorso del file di override:** `/etc/systemd/system/ollama.service.d/override.conf`

### Procedura di modifica:
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

## 🚀 2. Gestione dei Modelli
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

## 📊 3. Monitoraggio Hardware (GPU AMD)
Il monitoraggio deve essere effettuato specificamente sul **Bus 03** per verificare l'effettivo utilizzo della scheda dedicata.

### Verifica del carico (Radeontop)
L'utilizzo della GPU può essere osservato tramite il comando:
```bash
sudo radeontop -b 03
```
Si consiglia di monitorare la voce `Graphics pipe` per l'attività di calcolo e `VRAM` per l'allocazione della memoria.

### Statistiche ROCm (SMI)
Per un controllo puntuale di temperature e frequenze:
```bash
watch -n 0.5 rocm-smi
```

---

## 🛠 4. Diagnostica e FAQ

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

## 🛠️ 5. Ecosistema di Strumenti Avanzati (Oltre la Chat)

L'utilizzo di Ollama tramite terminale è solo il punto di partenza. Per sfruttare appieno la potenza di calcolo della GPU AMD, è opportuno integrare strumenti che trasformino il modello linguistico in un agente operativo.

### Perché utilizzare strumenti diversi?
Ogni interfaccia gestisce i **Token di Contesto** e la **VRAM** in modo differente:
- Le **WebUI** sono ideali per la conversazione generale.
- I **Sistemi RAG** (AnythingLLM) servono per consultare grandi moli di dati senza saturare la memoria video.
- Gli **Agenti CLI** (Aider) servono per l'interazione diretta con il file system e il codice.

---

### 📚 5.1. AnythingLLM: Il Gestore della Conoscenza (RAG)
**AnythingLLM** è la soluzione definitiva per chi deve analizzare documenti (PDF, TXT, DOCX) in locale. 

### Perché conservarlo nel sistema:
1. **Efficienza VRAM:** Utilizza una tecnica di recupero (RAG) che invia alla GPU solo i frammenti di testo necessari per rispondere, permettendo di "interrogare" libri di migliaia di pagine su una scheda da 8GB.
2. **Workspace Isolati:** Permette di creare aree di lavoro separate (es. "Lavoro", "Studio", "Documentazione Tecnica").
3. **Privacy Totale:** Tutto il processo di indicizzazione avviene offline su Ubuntu.

**Utilizzo ideale:** Consultazione di manuali, analisi di contratti, studio di documentazione tecnica complessa.
*Nota: AnythingLLM non modifica i file, funge da lettore esperto.*

---

### 💻 5.2. Aider: L'Assistente alla Programmazione (AI Pair Programmer)
**Aider** è uno strumento da terminale che trasforma il modello (es. `qwen2.5-coder`) in un vero collaboratore capace di scrivere codice.



### Perché conservarlo nel sistema:
1. **Accesso al File System:** A differenza delle chat comuni, Aider può creare nuovi file e modificare quelli esistenti direttamente nelle cartelle di progetto.
2. **Integrazione Git:** Ogni modifica suggerita dall'AI può essere automaticamente seguita da un "commit", mantenendo traccia della cronologia del lavoro.
3. **Risparmio Risorse:** Non avendo interfaccia grafica, lascia il 100% della memoria della RX 6600 disponibile per il ragionamento del modello.

**Utilizzo ideale:** Scrittura di script Python, creazione di siti web, automazione di task su Ubuntu, correzione di bug.

---

### 📋 5.3. Sintesi delle Soluzioni Consigliate

Si consiglia di mantenere entrambi i sistemi installati per coprire ogni esigenza operativa:

| Strumento | Scopo Principale | Interazione con i File | Piattaforma |
| :--- | :--- | :--- | :--- |
| **AnythingLLM** | Studio e Ricerca | **Sola Lettura** (Analisi documenti) | AppImage / Desktop |
| **Aider** | Sviluppo Software | **Scrittura/Modifica** (Editing attivo) | Terminale (Python/Pip) |
| **Ollama (Base)** | Motore di calcolo | N/A (Fornisce l'intelligenza) | systemctl (Backend) |

---
