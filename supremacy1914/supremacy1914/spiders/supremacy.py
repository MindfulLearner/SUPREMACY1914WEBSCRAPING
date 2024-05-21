import scrapy
import os

class SupremacySpider(scrapy.Spider):
    name = "supremacy"
    allowed_domains = ["supremacy1914.com"]

    def start_requests(self):
        # Percorso completo al file HTML temporaneo
        file_path = os.path.join(os.path.dirname(__file__), 'temp_supremacy.html')
        self.logger.debug(f"Trying to open file at: {file_path}")
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                html_content = file.read()
                # Passa il contenuto HTML al metodo parse
                yield scrapy.http.TextResponse(url='file://localhost', body=html_content, encoding='utf-8')
        except FileNotFoundError:
            self.logger.error(f"File not found: {file_path}")

    def parse(self, response):
        # Trova i nomi dei giocatori utilizzando il selettore CSS fornito
        player_elements = response.css('.text_player_name::text')
        player_names = [element.get().strip() for element in player_elements]

        # Debug: stampa il numero di elementi trovati
        self.logger.debug(f"Number of player elements found: {len(player_elements)}")

        if player_names:
            with open("player_names.txt", "w", encoding="utf-8") as file:
                for name in player_names:
                    file.write(name + "\n")
            self.logger.debug("Player names have been saved to player_names.txt")
        else:
            self.logger.debug("No player names found with the given selector.")

        # Trova tutti i tag unici nella pagina
        unique_tags = set(response.xpath('//*').xpath('name()').getall())
        with open("unique_tags.txt", "w", encoding="utf-8") as file:
            for tag in unique_tags:
                file.write(tag + "\n")
        self.logger.debug("Unique tags have been saved to unique_tags.txt")
