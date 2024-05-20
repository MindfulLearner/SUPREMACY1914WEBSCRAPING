import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import os
import time

class SupremacySpider(scrapy.Spider):
    name = "supremacy"
    start_urls = ['https://www.supremacy1914.com/']

    def __init__(self):
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    def parse(self, response):
        self.driver.get(response.url)
        
        # Esegui il login
        username = os.getenv('USERNAME')
        password = os.getenv('PASSWORD')
        
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password + Keys.RETURN)
        
        # Attendi il completamento del login
        time.sleep(5)
        
        # Richiedi l'URL della partita dall'utente
        game_url = input("Inserisci l'URL della partita: ")
        
        # Naviga verso l'URL della partita
        self.driver.get(game_url)
        
        # Esegui lo scraping della pagina della partita
        time.sleep(5)  # Attendi il caricamento della pagina
        
        players = self.driver.find_elements(By.XPATH, '//div[@class="player"]')
        for player in players:
            name = player.find_element(By.XPATH, './/h2').text
            score = player.find_element(By.XPATH, './/span[@class="score"]').text
            coalition = player.find_element(By.XPATH, './/span[@class="coalition"]').text
            yield {
                'name': name,
                'score': score,
                'coalition': coalition
            }
        
        self.driver.quit()
