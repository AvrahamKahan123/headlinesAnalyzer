import psycopg2
from headlines.webscraper import *
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


def query_single_field(query: str, connection=get_db_connection()):
    """ Returns first field. Insert statement should be of form SELECT columnname from... Will return None if no matches"""
    cursor = connection.cursor()
    cursor.execute(query)
    result = cursor.fetchone()
    if result:
        return cursor.fetchone()[0]


def query_full_row(query: str, connection=get_db_connection()):
    cursor = connection.cursor()
    cursor.execute(query)
    return cursor.fetchone()


def link_headline_pnoun(headline_id: int, pNoun_id: int, connection=get_db_connection()):
    insert_stmt = f"INSERT INTO headlinePnouns(headlineId, pNounId) Values ({headline_id}, {pNoun_id})"
    execute_insert(insert_stmt, connection)


def add_headlines_SQLdb(headline_connection):
    """ adds headline to PostgreSQL database """
    cursor = headline_connection.cursor()
    headlines = get_all_headlines()
    insert_statements = [headline.create_insert() for headline in headlines]
    for add_query in insert_statements:
        cursor.execute(add_query)
    headline_connection.commit()

def get_highest_headline_ID(connection=get_db_connection()):
    query_highest = f"SELECT MAX(ID) from allheadlines"
    return query_single_field(query_highest, connection)

def get_highest_pNoun_id(connection=get_db_connection()):
    query_highest = f"SELECT MAX(ID) from ProperNouns"
    return query_single_field(query_highest, connection)

def update_DB():
    """ Updates Postgres with latest headlines"""
    connection = get_db_connection()
    with connection:
        with connection.cursor() as cursor:
            add_headlines_SQLdb(connection)
    connection.close()


if __name__ == '__main__':
    update_DB()
