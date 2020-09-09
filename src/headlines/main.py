import sys
from headlines.psql_util import get_db_connection
from headlines.psql_util import execute_multiple_inserts
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


class InvalidArgumentException(Exception):
    pass


if __name__ == '__main__':
    if len(sys.argv == 1):
        raise InvalidArgumentException("Invalid arguments supplied to main.py")
    elif sys.argv[2] == "update":
        update_DB()
        print("DATABASE UPDATED SUCCESFULLY")
        sys.exit(0)
    elif sys.argv[2] == "analyze":
        pass # will be code to cluster and analyze titles
        print("HEADLINES ANALYZED")
