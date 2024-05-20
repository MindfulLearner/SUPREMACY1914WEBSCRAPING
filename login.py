import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Carica le variabili d'ambiente dal file .env
load_dotenv()

# Ottieni le variabili d'ambiente
username = os.getenv('USERNAME')
password = os.getenv('PASSWORD')

# Configura il driver
driver = webdriver.Chrome()
driver.get('https://www.supremacy1914.it/')

# Aspetta che la pagina sia completamente caricata
wait = WebDriverWait(driver, 10)

# Trova e clicca il pulsante di login
login_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@class="btn btn-primary btn-lg" and contains(text(),"Entra")]')))
login_button.click()

# Inserisci username e password
username_input = wait.until(EC.presence_of_element_located((By.NAME, 'username')))
password_input = wait.until(EC.presence_of_element_located((By.NAME, 'password')))

username_input.send_keys(username)
password_input.send_keys(password)

# Trova e clicca il pulsante per inviare il form di login
submit_button = driver.find_element(By.XPATH, '//button[@type="submit"]')
submit_button.click()

# Aggiungi qui il resto del tuo codice di scraping

# Chiudi il driver
driver.quit()
