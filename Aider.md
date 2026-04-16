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
**VRAM:** Poiché il browser avviato da Playwright viene utilizzato per il "web scraping" testuale, l'impatto sulla VRAM è trascurabile.

### Installazione e Configurazione
Qualora non fosse presente nel sistema, l'ambiente viene predisposto tramite i seguenti comandi:

```bash
python3 -m pip install playwright

# Installazione dei binari del browser necessari
playwright install chromium
```

### ⚠️ Requisito: Git
L'interfaccia grafica (`--browser`) richiede obbligatoriamente che la cartella di lavoro sia un repository **Git** inizializzato. 
- **Risoluzione:** Eseguire `git init` nella cartella di progetto prima di lanciare Aider, aggiungere un branch main e fare una prima commit di inizializzazione.
- **Vantaggio:** Questo permette alla GUI di gestire i rollback, mostrare i "diff" visivi e garantire la sicurezza del codice sorgente.