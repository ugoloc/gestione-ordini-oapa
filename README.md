# gestione-ordini-oapa

@author: Ugo Lo Cicero
@version: 1.0
@date: 2022 (first release: 2015)
@coding: Python
@summary: Questo software, basato su framework Django, è stato sviluppato per la gestione delle procedure di acquisto di INAF-Osservatorio Astronomico di Palermo, soddisfacendo l'esigenza di digitalizzare un processo multistep che richiede una sequenza di autorizzazioni e "firme". L'interfaccia utente è una web-app accessibile remotamente con autenticazione. Utilizza un database per raccogliere le informazioni sugli utenti abilitati e sulle procedure in atto e concluse. Ogni procedura consiste in una sequenza di sezioni, costituite da form, che possono essere compilate esclusivamente dai responsabili assegnati. E' possibile inserire allegati in ciascuna sezione. Le sezioni possono essere salvate per essere completate successivamente. Quando una sezione viene finalizzata (chiusa), il software invia una notifica email ai responsabili della successiva sezione aperta. Le sezioni possono essere chiuse in ordine sparso secondo esigenza, sebbene la sequenza rifletta il flusso ordinario di lavorazione. Una sezione chiusa può essere riaperta dal responsabile della sezione successiva. Le sezioni di una procedura vengono visualizzate in sequenza in una singola pagina web, con un menu di navigazione laterale che consente di avere una panoramica dello stato di chiusura delle sezioni e di saltare ad una sezione specifica. La struttura del software è flessibile, per consentire facili variazioni al flusso della procedura, alle sezioni e ai campi presenti nelle sezioni. In caso di aggiornamento del flusso di procedura viene assegnata una nuova versione e viene mantenuto il supporto a ordini ancora aperti con versione di procedura precedente. Determinati campi o intere sezioni possono essere mostrate o meno in funzione di valori selezionati in sezioni precedenti, in modo da consentire flussi alternativi, o l'inserimento di informazioni diverse, per differenti casistiche (es. gare piuttosto che affidamento diretto, oppure ordine tramite MEPA o meno). Il software è stato adottato stabilmente dalla struttura OAPA a partire da giugno 2015.

@features:
- Login con username e password.
- Gruppi di utenti con speciali privilegi: Direzione, responsabili d'ufficio, RUP, responsabili di fondi.
- Super-utenti per effettuare modifiche dirette.
- Lista di procedure in DB ordinabile, con visibilità dello stato dell'ordine (aperto, inviato, chiuso, annullato...), indicazione del responsabile della prima sezione aperta e funzioni di ricerca su vari campi.
- Gestione della responsabilità delle sezioni, con autorizzazioni relative per modifiche, chiusure, riaperture.
- Notifiche email al personale coinvolto per ogni chiusura di sezione.
- Possibilità per qualsiasi utente registrato di seguire un ordine, ricevendo notifiche email per ogni chiusura di sezione.
- Possibilità di allegare file ad ogni sezione, con descrizione relativa.
- Possibilità di compilazione automatica di moduli in PDF in base ai campi compilati nelle sezioni (es. per generazione della determina di acquisto).
- Gestione dell'annullamento di procedure di ordine.
- Gestione di una lista di progetti e relativi obiettivi funzione per caricamento rapido dei dati nelle sezioni.
- Gestione di multiple versioni di flusso di procedura.
- Determinati campi o intere sezioni possono essere mostrate o meno in funzione di valori selezionati in sezioni precedenti
- Produzione di informazioni per generare i report di trasparenza.
- Supporta diversi tipi di DB (PostgreSQL, mySQL...)

@notes:
Per rendere operativo il software è necessario:
- creare un DB di supporto
- configurare il file settings.py
- predisporre un webserver di supporto (es. apache con mod_wsgi)
