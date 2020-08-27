from commit_headlinesDB import database_connector
from commit_headlinesDB.webscraper import *
from typing import List
from headlines.article_headline import ArticleHeadline


def get_all_headlines() -> List[str]:
    """ Returns list of all headlines currently being scraped """
    all_headlines = [ArticleHeadline(headline, 'FOX') for headline in get_FOX_headlines()]
    all_headlines.extend([ArticleHeadline(headline, 'MSNBC') for headline in get_MSNBC_headlines()])
    all_headlines.extend([ArticleHeadline(headline, 'ABC') for headline in get_ABC_headlines()])
    return all_headlines


def add_headlines_SQLdb(headline_connection):
    """ adds headline to PostgreSQL database """
    cursor = headline_connection.cursor()
    headlines = get_all_headlines()
    insert_statements = [create_insert_statement(headline) for headline in headlines]
    for add_query in insert_statements:
        cursor.execute(add_query)
    headline_connection.commit()


def create_insert_statement(headline: ArticleHeadline)  -> str:
    """ Returns insert statement for article """
    return f"INSERT into allheadlines(newsorg, title, articledate, articletime) values('{headline.source}', '{headline.title}', CURRENT_DATE, CURRENT_TIME) ON CONFLICT DO NOTHING;"


def update_DB():
    """ Updates Postgres with latest headlines"""
    connection = database_connector.get_db_connection()
    with connection:
        with connection.cursor() as cursor:
            add_headlines_SQLdb(connection)
    connection.close()

if __name__ == '__main__':
    update_DB()
