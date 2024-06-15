import scrapy
import json
from scrapy.crawler import CrawlerProcess

from items import OzonItem
from ozon.pipelines import SqliteDemoPipeline


class OzonSpider(scrapy.Spider):
    name = "quotes"
    start_urls = [
        'https://www.ozon.ru/product/kapsuly-dlya-kofemashin-tassimo-coffee-shop-selections-toffee-nut-latte-1447885502/?asb=Gfki8AqPzPLkMrI6Z18%252B2bYqQoyAF9huycbVBTSTXtY%253D&asb2=bk2o6Tcg0n1HLDxqUcSBFL1eF0MVinJRP2LRnuNJ2Cij4U92IsqRDhx_GRpIJq28&avtc=1&avte=2&avts=1718389261&keywords=tassimo+latte'
    ]

    def parse(self, response):
        for webPrice in response.css("div[data-widget='webPrice']"):
            yield {
                "webPrice": webPrice.css("span::text").get(),
            }

        next_page = response.css('li.next a::attr("href")').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)


class OzonItemsSpider(scrapy.Spider):
    name = "ozon_items"
    start_urls = [
        'https://api.ozon.ru/composer-api.bx/page/json/v2?url=https://www.ozon.ru/category/produkty-pitaniya-9200/?text=tassimo+capuchino',
        'https://api.ozon.ru/composer-api.bx/page/json/v2?url=https://www.ozon.ru/category/produkty-pitaniya-9200/?text=tassimo+latte',
    ]

    def parse(self, response):
        data = json.loads(response.text)
        widgetStates = data["widgetStates"]
        if False:
            with open('ozon_1.json', 'w', encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=False)
        for attribute, value in widgetStates.items():
            if str(attribute).startswith('searchResultsV2'):
                search_result = json.loads(value)
                items = search_result["items"]
                for item in items:
                    ozon_item = OzonItem()
                    ozon_item['start_url'] = response.url.replace('https://api.ozon.ru/composer-api.bx/page/json/v2?url=', '')
                    ozon_item['skuId'] = item['skuId']
                    ozon_item['link'] = item['action']['link']

                    main_state = item['mainState']
                    ozon_item["price"] = str(main_state[0]['atom']['priceV2']['price'][0]['text']).replace(
                        "\u2009", "").replace("₽", "")
                    try:
                        if len(main_state) == 2:
                            ozon_item["name"] = str(main_state[1]['atom']['textAtom']['text']).replace("\n", "")
                        elif len(main_state) >= 2:
                            ozon_item["name"] = str(main_state[2]['atom']['textAtom']['text']).replace("\n", "")
                        yield ozon_item
                    except (IndexError):
                        print(main_state)


def main():
    process = CrawlerProcess(settings={
        "ITEM_PIPELINES": {
            SqliteDemoPipeline: 300,
        }
    })
    process.crawl(OzonItemsSpider)
    process.start()


if __name__ == '__main__':
    main()
