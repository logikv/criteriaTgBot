import sqlite3


class SqliteDemoPipeline:

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
             start_url TEXT NOT NULL
         )
         """)

    def process_item(self, item, spider):

        self.cur.execute("select price from ozon where skuId = " + str(item['skuId']))
        result = self.cur.fetchone()
        ## If it is in DB, create log message
        if result:
            spider.logger.warn("Item already in database: %s" % item['skuId'])
            if int(result[0]) != int(item['price']):
                self.cur.execute(
                    "UPDATE items SET price =" + int(item['price']) + " WHERE skuId = " + str(item['skuId']))
                self.con.commit()
        else:
            self.cur.execute("""
                     INSERT INTO items (skuId, name, price, link,  start_url) VALUES (?, ?, ?, ?, ?)
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
