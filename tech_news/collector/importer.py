import csv
import re


def dict_fetcher(data, headers):
    news_list = []
    for news in data:
        news_list.append(
            {header: news[index] for index, header in enumerate(headers)}
        )
    return news_list


def header_checker(headers):
    expected_headers = ['url', 'title', 'timestamp', 'writer', 'shares_count',
                        'comments_count', 'summary', 'sources', 'categories']
    if not all(item in expected_headers for item in headers):
        raise ValueError('Headers invalidos')


def csv_importer(filepath, fetcher=dict_fetcher):
    if not re.search('.csv', filepath):
        raise ValueError('Formato invalido')
    try:
        with open(filepath) as file:
            news_list = csv.reader(file, delimiter=';', quotechar='"')
            headers, *data = news_list
        header_checker(headers)
    except FileNotFoundError:
        if not re.search('.csv', filepath):
            raise ValueError('Formato inválido')
        else:
            filename = re.search(r'\/(.*.csv)', filepath).group(1)
            raise ValueError(f'Arquivo {filename} não encontrado')
    else:
        return fetcher(data, headers)


if __name__ == '__main__':
    print(csv_importer('file_csv.csv'))
