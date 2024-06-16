from scrapy.crawler import CrawlerProcess

from ozon.hunter.myscrapy import OzonApiItemsSpider
from ozon.hunter.pipelines import StoreInDatabasePipeline, NotificationPipeline
from ozon.hunter.settings import settings

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
    links = []
    for setting in settings:
        links.append(setting['link'])
    OzonApiItemsSpider.start_urls = links
    OzonApiItemsSpider.custom_settings = {
        'settings': settings
    }
    process.crawl(OzonApiItemsSpider)


def main():
    construct_process()
    start_process()


if __name__ == '__main__':
    main()
