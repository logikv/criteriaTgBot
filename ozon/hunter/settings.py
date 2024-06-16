settings = [
    {
        'name': 'tassimo+capuchino',
        'link': 'https://api.ozon.ru/composer-api.bx/page/json/v2?url=https://www.ozon.ru/category/produkty-pitaniya-9200/?text=tassimo+capuchino',
        'price': 600
    },
    {
        'name': 'tassimo+latte',
        'link': 'https://api.ozon.ru/composer-api.bx/page/json/v2?url=https://www.ozon.ru/category/produkty-pitaniya-9200/?text=tassimo+latte',
        'price': 600
    }
]


def found_by_start_link(some_settings, start_link):
    for setting in some_settings:
        if setting['link'].replace('https://api.ozon.ru/composer-api.bx/page/json/v2?url=', '') == start_link:
            return setting
