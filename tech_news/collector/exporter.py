import re
import csv

from tech_news.database import find_news


def csv_exporter(filepath):
    headers = ['url', 'title', 'timestamp', 'writer', 'shares_count',
               'comments_count', 'summary', 'sources', 'categories']
    if not re.search('.csv', filepath):
        raise ValueError('Formato invalido')
    with open(filepath, 'w', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=';', quotechar='"')
        writer.writerow(headers)
        news_list = find_news()
        for news in news_list:
            data = list(news.values())
            for index, value in enumerate(data):
                if(isinstance(value, list)):
                    data[index] = ','.join([*value])
            writer.writerow(data)


csv_exporter('teste.csv')
