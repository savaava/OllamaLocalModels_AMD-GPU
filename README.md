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

# 🛠️ 5. Ecosistema di Strumenti Avanzati (Oltre la Chat)

L'utilizzo di Ollama tramite terminale è solo il punto di partenza. Per sfruttare appieno la potenza di calcolo della GPU AMD, è opportuno integrare strumenti che trasformino il modello linguistico in un agente operativo.

### Perché utilizzare strumenti diversi?
Ogni interfaccia gestisce i **Token di Contesto** e la **VRAM** in modo differente:
- Le **WebUI** sono ideali per la conversazione generale.
- I **Sistemi RAG** (AnythingLLM) servono per consultare grandi moli di dati senza saturare la memoria video.
- Gli **Agenti CLI** (Aider) servono per l'interazione diretta con il file system e il codice.

---

## 📚 5.1. AnythingLLM: Il Gestore della Conoscenza (RAG)
**AnythingLLM** è la soluzione definitiva per chi deve analizzare documenti (PDF, TXT, DOCX) in locale. 

### Perché conservarlo nel sistema:
1. **Efficienza VRAM:** Utilizza una tecnica di recupero (RAG) che invia alla GPU solo i frammenti di testo necessari per rispondere, permettendo di "interrogare" libri di migliaia di pagine su una scheda da 8GB.
2. **Workspace Isolati:** Permette di creare aree di lavoro separate (es. "Lavoro", "Studio", "Documentazione Tecnica").
3. **Privacy Totale:** Tutto il processo di indicizzazione avviene offline su Ubuntu.

**Utilizzo ideale:** Consultazione di manuali, analisi di contratti, studio di documentazione tecnica complessa.
*Nota: AnythingLLM non modifica i file, funge da lettore esperto.*

---

## 💻 5.2. Aider: L'Assistente alla Programmazione (AI Pair Programmer)
**Aider** è uno strumento da terminale che trasforma il modello (es. `qwen2.5-coder`) in un vero collaboratore capace di scrivere codice.



### Perché conservarlo nel sistema:
1. **Accesso al File System:** A differenza delle chat comuni, Aider può creare nuovi file e modificare quelli esistenti direttamente nelle cartelle di progetto.
2. **Integrazione Git:** Ogni modifica suggerita dall'AI può essere automaticamente seguita da un "commit", mantenendo traccia della cronologia del lavoro.
3. **Risparmio Risorse:** Non avendo interfaccia grafica, lascia il 100% della memoria della RX 6600 disponibile per il ragionamento del modello.

**Utilizzo ideale:** Scrittura di script Python, creazione di siti web, automazione di task su Ubuntu, correzione di bug.

---

## 📋 5.3. Sintesi delle Soluzioni Consigliate

Si consiglia di mantenere entrambi i sistemi installati per coprire ogni esigenza operativa:

| Strumento | Scopo Principale | Interazione con i File | Piattaforma |
| :--- | :--- | :--- | :--- |
| **AnythingLLM** | Studio e Ricerca | **Sola Lettura** (Analisi documenti) | AppImage / Desktop |
| **Aider** | Sviluppo Software | **Scrittura/Modifica** (Editing attivo) | Terminale (Python/Pip) |
| **Ollama (Base)** | Motore di calcolo | N/A (Fornisce l'intelligenza) | systemctl (Backend) |

---

# 💻 6. Guida Operativa all'uso di Aider (CLI)

L'interazione con Aider avviene tramite una sessione interattiva nel terminale. Per garantire l'efficienza del modello e il risparmio della VRAM sulla GPU dedicata, viene raccomandato l'uso dei seguenti comandi di controllo (slash commands).

###Avvio della Sessione
L'esecuzione deve essere preceduta dall'ingresso nella cartella di progetto:
```bash
aider --model ollama/qwen2.5-coder:7b
```

## Comandi di Gestione Contesto e File
All'interno della sessione di Aider (prompt `>`), è possibile utilizzare i seguenti comandi per gestire i file e la memoria video:

| Comando | Funzione |
| :--- | :--- |
| `/add <file>` | Aggiunge uno o più file al contesto di modifica (l'AI può leggerli e scriverli). |
| `/read-only <file>` | Aggiunge file in sola lettura (utile per fornire documentazione senza modifiche). |
| `/drop <file>` | Rimuove un file dal contesto per liberare spazio nella finestra dei token. |
| `/ls` | Elenca tutti i file attualmente inclusi nella sessione. |

## Comandi di Sviluppo e Controllo
| Comando | Funzione |
| :--- | :--- |
| `/undo` | Annulla l'ultima modifica apportata ai file e l'ultimo commit Git. |
| `/diff` | Mostra le differenze (modifiche proposte) tra lo stato attuale e l'ultimo commit. |
| `/commit` | Forza un commit Git delle modifiche correnti (se non automatico). |
| `/run <comando>` | Esegue un comando shell (es. test unitari) e invia l'output all'AI per analisi. |
| `/exit` | Termina la sessione e chiude l'interfaccia CLI. |

## Modalità di Interazione Avanzata
In contesti di architettura complessa o con limiti di memoria video (8GB), si consiglia l'uso della modalità discussione:
* **`/architect`**: Avvia una fase di pianificazione senza scrivere codice, utile per definire la struttura prima dell'implementazione.
* **`/ask`**: Pone domande sul codice esistente senza richiedere modifiche dirette ai file.

## 🌐 Utilizzo dell'Interfaccia Grafica (Browser GUI)
È possibile utilizzare Aider anche attraverso un'interfaccia grafica (GUI) basata su browser. Questa modalità è utile per chi preferisce una visualizzazione più chiara dei file e delle modifiche rispetto al solo terminale, pur mantenendo tutta la potenza del motore locale basato su Ollama.

Sebbene Aider nasca come strumento da riga di comando, è prevista una modalità grafica che permette di gestire i file e la chat attraverso il browser di sistema.

### Avvio della modalità GUI
Per avviare l'interfaccia grafica, è necessario aggiungere il flag `--browser` al comando di avvio:

```bash
aider --model ollama/qwen2.5-coder:7b --browser
```

### Attenzione
L'interfaccia grafica (GUI) di Aider non è solo una finestra di chat, ma un vero e proprio pannello di controllo per le modifiche ai file. Poiché Aider usa Git per gestire i rollback (/undo), mostrare le differenze (diff) e garantire che il codice non venga corrotto, la GUI si rifiuta di avviarsi se non rileva un repository attivo:
```bash
cd ~/tuo_progetto
git init
aider --model ollama/qwen2.5-coder:7b --browser
```

### Caratteristiche dell'interfaccia web:
- **Gestione File facilitata:** È possibile aggiungere o rimuovere file dal contesto di lavoro tramite menu a tendina o icone dedicate, senza dover digitare i percorsi completi.
- **Anteprima delle modifiche:** Le differenze (diff) tra il codice originale e quello generato dall'IA vengono evidenziate graficamente con i classici colori rosso (rimozioni) e verde (aggiunte).
- L'utilizzo della modalità `--browser` su Ubuntu 22.04 comporta un leggero aumento del consumo di risorse

## 🔍 Integrazione Web con Playwright

Per estendere le capacità di analisi, Aider può utilizzare **Playwright**, una libreria di automazione del browser che permette all'intelligenza artificiale di "leggere" contenuti direttamente dal web.

### Utilità di Playwright in Aider
L'integrazione di Playwright consente al modello di:
1. **Consultare Documentazione Online:** L'AI può accedere a siti web (es. documentazione ufficiale di librerie Python o framework JS) per ottenere esempi di codice aggiornati che non sono presenti nel suo dataset di addestramento originale.
2. **Analizzare URL Specifici:** È possibile fornire ad Aider un indirizzo web affinché lo analizzi e utilizzi le informazioni contenute per scrivere o correggere il codice locale.
3. **Modalità Headless:** Su Ubuntu 22.04, Playwright opera solitamente in modalità "headless" (senza finestra visibile), ottimizzando l'uso delle risorse di sistema.

### Installazione e Configurazione
Qualora non fosse presente nel sistema, l'ambiente viene predisposto tramite i seguenti comandi:

```bash
# Installazione della libreria Python
python3 -m pip install playwright

# Installazione dei binari del browser necessari
playwright install chromium
```

### ⚠️ Requisito Mandatorio: Git
L'interfaccia grafica (`--browser`) richiede obbligatoriamente che la cartella di lavoro sia un repository **Git** inizializzato. 
- Se la cartella non è sotto controllo di versione, la GUI non verrà avviata.
- **Risoluzione:** Eseguire `git init` nella cartella di progetto prima di lanciare Aider.
- **Vantaggio:** Questo permette alla GUI di gestire i rollback, mostrare i "diff" visivi e garantire la sicurezza del codice sorgente.

### Impatto sulle Risorse
L'attivazione di Playwright durante una sessione di Aider comporta l'avvio temporaneo di un'istanza di Chromium. 
- **CPU/RAM:** Si verifica un picco temporaneo nell'uso del processore e della RAM durante il caricamento delle pagine web.
- **VRAM:** Poiché il browser avviato da Playwright viene utilizzato per il "web scraping" testuale, l'impatto sulla memoria della **RX 6600** è trascurabile, lasciando quasi interamente gli 8GB a disposizione di Ollama.

# 📋 7. Riepilogo Accesso Strumenti

| Strumento | Modalità di Accesso | Comando/Eseguibile |
| :--- | :--- | :--- |
| **AnythingLLM** | Desktop (GUI) | `~/AnythingLLMDesktop.AppImage` |
| **Aider (Standard)** | Terminale (CLI) | `aider --model <nome_modello>` |
| **Aider (Visual)** | Browser (GUI) | `aider --model ollama/<nome_modello> --browser` |
| **Monitoraggio** | Terminale (CLI) | `sudo radeontop -b 03` |

# 🔄 8. Tabella di Manutenzione Totale
Ecco la tabella definitiva per la manutenzione dei tutti sistemi:

| Componente | Comando di Aggiornamento | Frequenza Consigliata |
| :--- | :--- | :--- |
| **Driver/Sistema** | `sudo apt update && sudo apt upgrade` | Settimanale |
| **Ollama (Core)** | `curl -fsSL https://ollama.com/install.sh \| sh` | Mensile |
| **Aider (Coding)** | `pip install --upgrade aider-chat` | Settimanale |
| **AnythingLLM** | Riesecuzione `./installer.sh` | Al rilascio (Notifica GUI) |
| **Modelli LLM** | `ollama pull <nome_modello>` | Quando disponibili update |
| **Web Scraping** | `playwright install chromium` | Solo se Aider lo richiede |
