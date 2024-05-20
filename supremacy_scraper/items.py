import scrapy

class PlayerItem(scrapy.Item):
    name = scrapy.Field()
    score = scrapy.Field()
    coalition = scrapy.Field()
