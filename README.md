# Supremacy 1914 Scraper

Questo progetto è un web scraper per il gioco Supremacy 1914. Utilizza Scrapy e Selenium per automatizzare il processo di accesso al gioco e raccogliere dati sulle partite. Il programma si connette a Google Chrome, accede al sito, inserisce le credenziali memorizzate in un file `.env` e richiede l'URL della partita per eseguire lo scraping dei dati.

## Obiettivi dello Scraper

- Automatizzare l'accesso a Supremacy 1914
- Raccogliere dati sui giocatori, punteggi e coalizioni
- Salvare i dati raccolti per ulteriori analisi

## Processo del Programma

1. Avvio di Google Chrome tramite Selenium
2. Accesso al sito [Supremacy 1914](https://www.supremacy1914.com)
3. Accesso con le credenziali memorizzate nel file `.env`
4. Sul terminale, viene richiesto di inserire l'URL della partita per iniziare lo scraping

## Installazione

1. Scaricare o clonare il repository (verrà pubblicato su [GitHub](https://github.com/ilovelearningthings/SUPREMACY1914WEBSCRAPING) non appena disponibile):
   ```bash
   git clone https://github.com/ilovelearningthings/SUPREMACY1914WEBSCRAPING.git
   cd SUPREMACY1914WEBSCRAPING
