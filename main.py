import schedule
import time


def run_crawler():
    from subprocess import check_output
    check_output("python ozon/crawl/crawler.py", shell=True).decode()


def run_tgbot():
    from subprocess import check_output
    check_output("python ozon/tg/bot.py", shell=False).decode()


def main():
    if True:
        run_crawler()
    else:
        schedule.every().minute.at(":15").do(run_crawler)
        while True:
            schedule.run_pending()
            time.sleep(1)


if __name__ == '__main__':
    main()
