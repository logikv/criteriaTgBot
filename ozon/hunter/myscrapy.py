import scrapy
import json

from ozon.hunter.items import OzonItem


def sanitize(string):
    return (str(string)
            .replace("\n", "")
            .replace("\u2009", ""))


def dump_json(data, file_name='ozon_1.json'):
    with open(file_name, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False)


class OzonApiItemsSpider(scrapy.Spider):
    name = "ozon_items"

    def parse(self, response):
        data = json.loads(response.text)
        widgetStates = data["widgetStates"]
        if False:
            dump_json(widgetStates)
        for attribute, value in widgetStates.items():
            if str(attribute).startswith('searchResultsV2'):
                search_result = json.loads(value)
                items = search_result["items"]
                for item in items:
                    ozon_item = OzonItem()
                    ozon_item['start_url'] = response.url.replace(
                        'https://api.ozon.ru/composer-api.bx/page/json/v2?url=', '')
                    ozon_item['skuId'] = item['skuId']
                    ozon_item['link'] = item['action']['link']

                    main_state = item['mainState']
                    ozon_item["price"] = str(main_state[0]['atom']['priceV2']['price'][0]['text']).replace("\u2009",
                                                                                                           "").replace(
                        "₽", "")
                    try:
                        for atom in main_state:
                            if atom['atom']['type'] == 'textAtom':
                                ozon_item["name"] = sanitize(atom['atom']['textAtom']['text'])

                        if ozon_item['name'] is None:
                            print(main_state)
                        yield ozon_item
                    except (IndexError, KeyError):
                        print(main_state)
