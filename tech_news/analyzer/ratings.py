from tech_news.database import fetch_top5_news, fetch_top5_categories


def news_fetcher(news_list):
    return [(news["title"], news["url"]) for news in news_list]


def top_5_news():
    news_list = fetch_top5_news()
    return news_fetcher(news_list)


def top_5_categories():
    news_list = fetch_top5_categories()
    categories_rank = [news["_id"] for news in news_list]
    return categories_rank


if __name__ == "__main__":
    print(top_5_news())
    print(top_5_categories())
