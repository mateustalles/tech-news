from tech_news.database import search_news
from datetime import datetime
import re


def news_fetcher(news_list):
    return [(news["title"], news["url"]) for news in news_list]


def search_by_title(title):
    query = {
        "title":
            {"$regex": title, "$options": "i"}
        }
    news_list = search_news(query)
    return news_fetcher(news_list)


def search_by_date(date):
    try:
        dateformat = '%Y-%m-%d'
        datetime.strptime(date, dateformat)
    except ValueError:
        raise ValueError('Data inválida')
    else:
        query = {
            "timestamp":
                {"$regex": date}
            }
        news_list = search_news(query)
        return news_fetcher(news_list)


def search_by_source(source):
    pattern = re.compile(source, re.IGNORECASE)
    query = {
        "sources":
            {"$in": [pattern]}
        }
    news_list = search_news(query)
    return news_fetcher(news_list)


def search_by_category(category):
    pattern = re.compile(category, re.IGNORECASE)
    query = {
        "categories":
            {"$in": [pattern]}
        }
    news_list = search_news(query)
    return news_fetcher(news_list)


if __name__ == '__main__':
    print(search_by_source('ResetEra'))
