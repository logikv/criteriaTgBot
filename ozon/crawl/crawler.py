from scrapy.crawler import CrawlerProcess

from ozon.crawl.myscrapy import OzonApiItemsSpider
from ozon.crawl.pipelines import StoreInDatabasePipeline, NotificationPipeline

process = CrawlerProcess(settings={
    "ITEM_PIPELINES": {
        StoreInDatabasePipeline: 300,
        NotificationPipeline: 300
    }
})


def start_process():
    global process
    process.start()


def construct_process():
    global process
    process = CrawlerProcess(settings={
        "ITEM_PIPELINES": {
            StoreInDatabasePipeline: 300,
            NotificationPipeline: 300
        }
    })
    OzonApiItemsSpider.start_urls = [
        'https://api.ozon.ru/composer-api.bx/page/json/v2?url=https://www.ozon.ru/category/produkty-pitaniya-9200/?text=tassimo+capuchino',
        'https://api.ozon.ru/composer-api.bx/page/json/v2?url=https://www.ozon.ru/category/produkty-pitaniya-9200/?text=tassimo+latte',
    ]
    process.crawl(OzonApiItemsSpider)


def main():
    construct_process()
    start_process()


if __name__ == '__main__':
    main()
