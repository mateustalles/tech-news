import time
import requests

from tech_news.database import create_news
from parsel import Selector


def extract_quantity(arg):
    if(len(arg) > 0):
        if(isinstance(arg, list)):
            return int(arg[0])
        else:
            return int(arg)
    else:
        return 0


def sleep(delay):
    return time.sleep(delay)


def fetch_content(url, timeout=3, delay=0.5):
    try:
        response = requests.get(url, timeout=timeout)
        status_code = response.status_code
        if(status_code != 200):
            return ''
        selector = Selector(text=response.text)
        request_result = selector.get()

        sleep(delay)

        return request_result
    except requests.exceptions.Timeout:
        return ''


def scrape(fetcher=fetch_content, pages=1):
    news_list = []

    while(pages > 0):
        news_items = Selector(
            text=fetcher(f'https://www.tecmundo.com.br/novidades?page={pages}')
        )
        pages = pages - 1

        for news in news_items.css(".tec--list__item"):
            url = news.css(".tec--card__thumb a::attr(href)").get()
            inner_selector = Selector(text=fetcher(url))
            news_list.append({
                "url":
                    url,
                "title":
                    inner_selector.css(".tec--article__header__title *::text")
                    .get(),
                "timestamp":
                    inner_selector.css("time::attr(datetime)")
                    .get(),
                "writer":
                    inner_selector.css('.tec--author__info__link *::text')
                    .get(),
                "shares_count":
                    extract_quantity(
                        inner_selector
                        .css('.z--container .tec--toolbar__item *::text')
                        .re('\\d')),
                "comments_count":
                    extract_quantity(
                        inner_selector.css('#js-comments-btn *::text')
                        .re('\\d')
                    ),
                "summary":
                    ''.join(
                        inner_selector
                        .css('.tec--article__body p:first-child *::text')
                        .getall()
                    ),
                "sources":
                    inner_selector.css('[class="tec--badge"]::text')
                    .getall(),
                "categories":
                    inner_selector
                    .css('[class="tec--badge tec--badge--primary"]::text')
                    .getall()
            })
    return news_list


if __name__ == "__main__":
    news_list = scrape(fetch_content)
    create_news(news_list)
