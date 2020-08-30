import psycopg2
from headlines.webscraper import *
from headlines.ArticleHeadline import Name
from headlines.webscraper import get_all_headlines

""" PSQL Utility class"""

def get_db_connection():
    """ :return a connection to PostgresSQL headlines database"""
    try:
        # can reveal password since is only on local network
        headlineConnection = psycopg2.connect(user = "adminheadlines",
                                      password = "abc123",
                                      host = "127.0.0.1",
                                      port = "5432",
                                      database = "headlines")
        return headlineConnection

    except (Exception, psycopg2.Error) as connection_error :
        print ("Error when attempting to connect to Headlines database", connection_error)


def execute_multiple_inserts(insert_stmts: List[str], connection=get_db_connection()):
    cursor = connection.cursor()
    for stmt in insert_stmts:
        cursor.execute(stmt)
    connection.commit()


def execute_insert(insert_stmt: str, connection=get_db_connection()): # default behavior is to create a new connection if an existing one is not used
    cursor = connection.cursor()
    cursor.execute(insert_stmt)
    connection.commit()


def query_single_field(query: str, connection):
    cursor = connection.cursor()
    cursor.execute(query)
    return query.fetchone()[0]


def query_full_row(query: str, connection):
    cursor = connection.cursor()
    cursor.execute(query)
    return cursor.fetchone()


def create_insert_article(headline: ArticleHeadline)  -> str:
    """ Returns insert statement for article """
    return f"INSERT into allheadlines(newsorg, title, articledate, articletime) values('{headline.source}', '{headline.title}', CURRENT_DATE, CURRENT_TIME) ON CONFLICT DO NOTHING;"

def link_headline_place(headline_id: int, place_id: int, connection):
    insert_stmt = f"INSERT INTO HeadlinePlaces(headlineId, placeId) values({headline_id}, {place_id})"
    execute_insert(insert_stmt)


def link_headline_person(headline_id: int, person_id: int, connection):
    insert_stmt = f"INSERT INTO HeadlinePlaces(headlineId, person_id) values({headline_id}, {person_id})"
    execute_insert(insert_stmt, connection)


def link_headline_org(headline_id: int, org_id: int, connection):
    insert_stmt = f"INSERT INTO HeadlinePlaces(headlineId, person_id) values({headline_id}, {org_id})"
    execute_insert(insert_stmt, connection)


def add_famous(n: Name, level: int, description: str, connection) -> int:
    """ Adds a name to the famousPeople PostgreSQL table"""
    insert_query = f"insert into famousPeople(level, lastName, firstName, Description) values({level}, {n.last_name}, {n.first_name}, '{description}'"
    execute_insert(insert_query, connection)


def add_headlines_SQLdb(headline_connection):
    """ adds headline to PostgreSQL database """
    cursor = headline_connection.cursor()
    headlines = get_all_headlines()
    insert_statements = [headline.create_insert() for headline in headlines]
    for add_query in insert_statements:
        cursor.execute(add_query)
    headline_connection.commit()


def update_DB():
    """ Updates Postgres with latest headlines"""
    connection = get_db_connection()
    with connection:
        with connection.cursor() as cursor:
            add_headlines_SQLdb(connection)
    connection.close()

if __name__ == '__main__':
    update_DB()
