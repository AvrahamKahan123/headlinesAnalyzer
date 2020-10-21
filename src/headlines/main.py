import sys
from datetime import datetime
from typing import List
from headlines.ArticleHeadline import ArticleHeadline
from headlines.ArticleHeadline import HeadlineParser
from headlines.psql_util import get_db_connection
from headlines.psql_util import execute_multiple_inserts
from headlines.psql_util import query_batch
from headlines.webscraper import get_all_headlines


def update_DB():
    """ Updates Postgres with latest headlines"""
    connection = get_db_connection()
    with connection:
        add_headlines_SQLdb(connection)
    connection.close()


def add_headlines_SQLdb(headline_connection):
    """ adds headline to PostgreSQL database """
    headlines = get_all_headlines()
    insert_statements = [headline.create_insert() for headline in headlines]
    execute_multiple_inserts(insert_statements, headline_connection)


def get_articles(start: datetime, end: datetime, connection) -> List[ArticleHeadline]:
    query = f"""SELECT * FROM allHeadlines WHERE articleDate > {str(start.date())} AND articleDate < {str(end.date())} AND
    articleTime > {str(start.time()).split(' ')[1]} AND articleTime < {str(end.time()).split(' ')[1]}"""
    all_articles = query_batch(query, connection)
    return [ArticleHeadline(row[2], row[1], row[0]) for row in all_articles]


class InvalidArgumentException(Exception):
    pass


def one_day_ago() -> datetime:
    """ Returns datetime object containing exactly one day ago's datetime"""
    today = datetime.now()
    delta = datetime.timedelta(days=1)
    return today - delta


if __name__ == '__main__':
    if len(sys.argv == 1):
        raise InvalidArgumentException("Invalid arguments supplied to main.py")
    elif sys.argv[1] == "update":
        update_DB()
        print("DATABASE UPDATED SUCCESFULLY")
        sys.exit(0)
    elif sys.argv[1] == "analyze":
        connection = get_db_connection()
        articles = get_articles(one_day_ago(), datetime.now()) # BUG: MAY REANALYZE ARTICLES. THIS WILL BE DEALT WITH
        analyzed = [HeadlineParser(article) for article in articles]
        # Use LDA to analyze, get tweets and add to elasticsearch
        print("HEADLINES ANALYZED")
