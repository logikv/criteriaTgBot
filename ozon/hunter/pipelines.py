import sqlite3

import telebot

from ozon.hunter.items import OzonItem
from ozon.hunter.settings import found_by_start_link


class StoreInDatabasePipeline:

    def __init__(self):
        ## Create/Connect to database
        self.con = sqlite3.connect('ozon_prices.db')

        ## Create cursor, used to execute commands
        self.cur = self.con.cursor()

        ## Create quotes table if none exists
        self.cur.execute("""
         CREATE TABLE IF NOT EXISTS items(
             skuId TEXT PRIMARY KEY,
             name TEXT NOT NULL,
             price INTEGER NOT NULL,
             link TEXT NOT NULL UNIQUE,
             start_url TEXT NOT NULL,
             last_touch DATE
         )
         """)

    def process_item(self, item, spider):

        self.cur.execute("SELECT price FROM items WHERE skuId = " + str(item['skuId']))
        result = self.cur.fetchone()
        ## If it is in DB, create log message
        if result:
            spider.logger.warn("Item already in database: %s" % item['skuId'])
            if int(result[0]) != int(item['price']):
                self.cur.execute(
                    "UPDATE items SET last_touch = datetime('now') and price =" + int(
                        item['price']) + " WHERE skuId = " + str(item['skuId']))
                self.con.commit()
        else:
            self.cur.execute("""
                     INSERT INTO items (skuId, name, price, link, start_url, last_touch) VALUES (?, ?, ?, ?, ?, datetime('now'))
                 """,
                             (
                                 str(item['skuId']),
                                 item['name'],
                                 item['price'],
                                 str(item['link']),
                                 item['start_url']
                             ))

            self.con.commit()
        return item


class NotificationPipeline():
    def __init__(self):
        print("tg notificator initialized")
        self.bot = telebot.TeleBot("6788334491:AAEgFkwX-2BgwBA1cOOltrI1prRcP0iNeso")

    def process_item(self, item, spider):
        settings = spider.custom_settings['settings']
        if type(item) is OzonItem:
            setting = found_by_start_link(settings, item['start_url'])
            if int(item['price']) <= int(setting['price']):
                spider.logger.info("found an item for good price")
                msg_str = f"""
                Товар: {item['name']}
                Ссылка: https://www.ozon.ru{item['link']}
                Цена: {item['price']}
                Поиск по: {setting['name']}
                """
                self.bot.send_message(chat_id="181553450", text=msg_str)
        return item
