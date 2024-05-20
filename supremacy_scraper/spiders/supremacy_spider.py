import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import os
import time

class SupremacySpider(scrapy.Spider):
    name = "supremacy"
    start_urls = ['https://www.supremacy1914.com/']

    def __init__(self):
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.wait = WebDriverWait(self.driver, 10)

    def parse(self, response):
        self.driver.get(response.url)
        
        # Accetta i cookies
        try:
            accept_cookies_button = self.wait.until(
                EC.element_to_be_clickable((By.ID, "didomi-notice-agree-button"))
            )
            time.sleep(2)  # Attendere un po' prima di cliccare
            accept_cookies_button.click()
            self.logger.info("Clicked on accept cookies button")
        except Exception as e:
            self.logger.error(f"Error accepting cookies: {e}")
        
        # Clicca sul pulsante "Entra" per aprire il form di login
        try:
            login_button = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, '//button[@class="btn btn-primary btn-lg" and contains(text(),"Entra")]'))
            )
            time.sleep(2)  # Attendere un po' prima di cliccare
            login_button.click()
            self.logger.info("Clicked on login button")
        except Exception as e:
            self.logger.error(f"Error clicking login button: {e}")
        
        # Esegui il login
        username = os.getenv('USERNAME')
        password = os.getenv('PASSWORD')
        
        try:
            username_input = self.wait.until(
                EC.presence_of_element_located((By.NAME, "username"))
            )
            password_input = self.driver.find_element(By.NAME, 'password')

            username_input.send_keys(username)
            password_input.send_keys(password + Keys.RETURN)
            self.logger.info("Entered login credentials")
            
            # Attendi il completamento del login
            time.sleep(5)
            
            # Richiedi l'URL della partita dall
        except Exception as e:
            self.logger.error(f"Error clicking login button: {e}")