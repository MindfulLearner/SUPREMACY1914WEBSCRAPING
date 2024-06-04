import os
import time
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv
import subprocess

# Funzione di login
def login(driver, username, password):
    driver.get("https://www.supremacy1914.it/")
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "didomi-notice-agree-button"))).click()
    username_input = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "loginbox_login_input")))
    password_input = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "loginbox_password_input")))
    username_input.send_keys(username)
    password_input.send_keys(password)
    login_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "func_loginbutton")))
    login_button.click()
    print("Login completato con successo!")

# Funzione per chiudere il popup utilizzando le coordinate
def chiusura_popup(driver):
    try:
        print("Attendo il caricamento della pagina di destinazione...")
        WebDriverWait(driver, 30).until(EC.url_contains("game.php?L=9&bust=1#/home/overview/"))
        time.sleep(2)  # Attendi 2 secondi per il caricamento del popup
        window_size = driver.get_window_size()
        actions = ActionChains(driver)
        # Calcola le coordinate relative alla finestra del browser
        x_offset = int(window_size['width'] * 0.75)
        y_offset = int(window_size['height'] * 0.5)
        actions.move_by_offset(x_offset, y_offset).click().perform()
        print("Popup chiuso con successo cliccando sulle coordinate!")
    except Exception as e:
        print(f"Errore durante il tentativo di chiudere il popup: {e}")

# Funzione per salvare il contenuto HTML della pagina in un file di testo
def save_html_content(driver, file_name):
    try:
        # Entra nell'iframe
        iframe = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "ifm"))
        )
        driver.switch_to.frame(iframe)
        print("Entrato nell'iframe del gioco.")
        
        # Salva il contenuto dell'iframe in un file di testo
        with open(file_name, 'w', encoding='utf-8') as file:
            file.write(driver.page_source)
        print(f"Contenuto HTML salvato con successo in {file_name}")
    except TimeoutException:
        print("Non è stato possibile trovare l'iframe del gioco.")
    finally:
        # Esce dall'iframe per poter navigare verso una nuova pagina
        driver.switch_to.default_content()

# Funzione di scraping
def scraping(driver):
    try:
        # Entra nell'iframe
        iframe = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "ifm"))
        )
        driver.switch_to.frame(iframe)
        print("Entrato nell'iframe del gioco.")
        
        # Ottiene il contenuto HTML della pagina
        html_content = driver.page_source
        
        # Avvia il processo Scrapy passando il contenuto HTML come argomento
        with open("temp_supremacy.html", "w", encoding="utf-8") as file:
            file.write(html_content)

        subprocess.run(["scrapy", "crawl", "supremacy"], check=True)

        print("Scraping completato con successo.")
    except TimeoutException:
        print("Non è stato possibile trovare i nomi dei giocatori nella pagina. Inserisci un URL valido.")
    finally:
        # Esce dall'iframe per poter navigare verso una nuova pagina
        driver.switch_to.default_content()

# Funzione di gestione
def manage_scraping(driver):
    url_set = False
    valid_url_pattern = re.compile(r"https://www.supremacy1914.com/game.php\?L=9&bust=1#/game/:gameID=\d+")
    
    while True:
        if not url_set:
            url = input("Inserisci l'URL della partita, 'scrap' per avviare lo scraping o digita 'stop' per terminare: ")
            if url.lower() == 'stop':
                print("Terminazione del programma richiesta dall'utente.")
                break
            if not valid_url_pattern.match(url):
                print("URL non valido. Inserisci un URL valido.")
                continue
            
            driver.get(url)
            print(f"Caricata la pagina: {url}")
            
            # Controlla se è rimasto sulla pagina overview, segno che l'URL non era valido
            time.sleep(5)  # Attendi 5 secondi per verificare il caricamento della pagina
            current_url = driver.current_url
            if "game.php?L=9&bust=1#/home/overview/" in current_url:
                print("URL non valido. Inserisci un URL valido.")
                continue
            
            url_set = True

        command = input("Digita 'scrap' per avviare lo scraping, 'url' per inserire un nuovo URL, 'save' per salvare il contenuto HTML o 'stop' per terminare: ")
        if command.lower() == 'stop':
            print("Terminazione del programma richiesta dall'utente.")
            break
        elif command.lower() == 'url':
            url_set = False
        elif command.lower() == 'scrap':
            scraping(driver)
        elif command.lower() == 'save':
            save_html_content(driver, 'pagina_supremacy1914.html')
        else:
            print("Comando non valido. Riprova.")

if __name__ == "__main__":
    main()

# Funzione principale
def main():
    load_dotenv()
    username = os.getenv("SUPREMACY_USERNAME")
    password = os.getenv("SUPREMACY_PASSWORD")
    if not username or not password:
        raise ValueError("Le variabili d'ambiente SUPREMACY_USERNAME e SUPREMACY_PASSWORD devono essere impostate")

    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    try:
        login(driver, username, password)
        chiusura_popup(driver)
        manage_scraping(driver)
    except Exception as e:
        print(f"Errore: {e}")
    finally:
        driver.quit()


