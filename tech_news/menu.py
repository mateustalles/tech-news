import sys

from tech_news.collector.importer import csv_importer
from tech_news.collector.exporter import csv_exporter
from tech_news.collector.scrapper import scrape, fetch_content
from tech_news.analyzer.ratings import top_5_news, top_5_categories
from tech_news.analyzer.search_engine import search_by_title, search_by_date
from tech_news.analyzer.search_engine import search_by_source
from tech_news.analyzer.search_engine import search_by_category


def create_news(data):
    return print(data)


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def collector_option_handler(option):
    def import_csv():
        print("Digite o nome do arquivo CSV a ser importado:")
        filepath = input()
        return create_news(csv_importer(filepath))

    def export_csv():
        print("Digite o nome do arquivo CSV a ser exportado:")
        filepath = input()
        return csv_exporter(filepath)

    def to_scrap():
        print("Digite a quantidade de páginas a serem raspadas:")
        pages = int(input())
        return create_news(scrape(fetcher=fetch_content, pages=pages))

    def to_quit():
        return print('Encerrando script\n')

    collector_options = {
        '1': import_csv,
        '2': export_csv,
        '3': to_scrap,
        '4': to_quit
    }

    return collector_options[option]()


def collector_menu():
    try:
        print("""Selecione uma das opções a seguir:
 1 - Importar notícias a partir de um arquivo CSV;
 2 - Exportar notícias para CSV;
 3 - Raspar notícias online;
 4 - Sair.""")
        option = input()
        collector_option_handler(option)
    except KeyError:
        return eprint('Opção inválida')


def search_title():
    print("Digite o título:")
    title = input()
    return create_news(search_by_title(title))


def search_date():
    print("Digite a data no formato aaaa-mm-dd:")
    date = input()
    return create_news(search_by_date(date))


def search_source():
    print("Digite a fonte:")
    source = input()
    return create_news(search_by_source(source))


def search_category():
    print("Digite a categoria:")
    category = input()
    return create_news(search_by_category(category))


def get_top_5_news():
    return create_news(top_5_news())


def get_top_5_categories():
    return create_news(top_5_categories())


def to_quit():
    return print('Encerrando script\n')


def analyzer_options_handler(option):
    analyzer_options = {
        '1': search_title,
        '2': search_date,
        '3': search_source,
        '4': search_category,
        '5': get_top_5_news,
        '6': get_top_5_categories,
        '7': to_quit
    }

    return analyzer_options[option]()


def analyzer_menu():
    try:
        print("""Selecione uma das opções a seguir:
 1 - Buscar notícias por título;
 2 - Buscar notícias por data;
 3 - Buscar notícias por fonte;
 4 - Buscar notícias por categoria;
 5 - Listar top 5 notícias;
 6 - Listar top 5 categorias;
 7 - Sair.""", end="")
        option = input()
        analyzer_options_handler(option)
    except KeyError:
        return eprint('Opção inválida')

# def create_news(function, **kwargs):
#     query_input = input()
#     if (kwargs["fetcher"]):
#         return function(fetcher=kwargs["fetcher"], pages=int(query_input))
#     return function(query_input)
