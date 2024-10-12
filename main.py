from requests_html import HTMLSession
from bs4 import BeautifulSoup
from typing import List
from settings import cookie
import json

START_URL = 'https://www.ozon.ru/seller/21vek-198419/krasota-i-zdorove-6500/?brand=135704519%2C18556218&miniapp=seller_198419&opened=brand'

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
    'accept': 'application/json',
    'cookie': cookie                #your cookie
}
PARAMS = {
    'layout_container': 'categorySearchMegapagination',
    'layout_page_index': 2,
    'page': 2,
}

session = HTMLSession()
session.headers.update(headers)


def get_products(s: HTMLSession, url: str, page: int = None) -> List[str] | None:
    response = s.get(url)
    soup = BeautifulSoup(response.text, 'lxml')

    if not page:
        div_id = 'state-searchResultsV2-3547917-default-1'
    else:
        div_id = f'state-searchResultsV2-193750-categorySearchMegapagination-{page}'

    data = soup.find('div', id=div_id)

    try:
        serialized_data = json.loads(data.get('data-state'))
    except AttributeError:
        return None

    return ['https://ozon.ru'+item.get('action').get('link') for item in serialized_data.get('items')]


def get_links(s: HTMLSession) -> List[str]:
    links = []
    links += get_products(s, START_URL)
    s.params = PARAMS

    while True:
        links_to_add = get_products(s, START_URL, PARAMS['page'])

        if not links_to_add:
            break

        links += links_to_add
        s.params['page'] += 1
        s.params['layout_page_index'] += 1

    return links


def ozon(s: HTMLSession):
    links = get_links(s)

    with open('ozon_ru.json', 'w') as f:
        json.dump(links, f)


if __name__ == '__main__':
    ozon(session)