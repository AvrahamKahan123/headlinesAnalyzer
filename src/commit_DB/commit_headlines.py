from commit_DB import database_connector
from commit_DB.webscraper import *
from headlines.article_headline import ArticleHeadline

def get_all_headlines() -> list ():
    all_headlines = [ArticleHeadline(headline, 'FOX') for headline in get_FOX_headlines()]
    all_headlines.extend([ArticleHeadline(headline, 'MSNBC') for headline in get_MSNBC_headlines()])
    all_headlines.extend([ArticleHeadline(headline, 'ABC') for headline in get_ABC_headlines()])
    return all_headlines

def add_headlines_SQLdb(headlineConnection, cursor):
    headlines = get_all_headlines()
    insert_statements = [create_insert_statement(headline) for headline in headlines]
    for add_query in insert_statements:
        cursor.execute(add_query)
    headlineConnection.commit()

def create_insert_statement(headline: ArticleHeadline)  -> list:
    return f"INSERT into allheadlines(newsorg, title, articledate, articletime) values('{headline.source}', '{headline.title}', CURRENT_DATE, CURRENT_TIME) ON CONFLICT DO NOTHING;"


def update_DB():
    connection = database_connector.get_db_connection()
    with connection:
        with connection.cursor() as cursor:
            add_headlines_SQLdb(connection, cursor)
    connection.close()

if __name__ == '__main__':
    a = get_all_headlines()
    for i in a:
        print(i)
