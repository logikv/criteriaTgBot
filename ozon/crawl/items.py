from scrapy.item import Item, Field


class OzonItem(Item):
    name = Field()
    price = Field()
    skuId = Field()
    link = Field()
    start_url = Field()