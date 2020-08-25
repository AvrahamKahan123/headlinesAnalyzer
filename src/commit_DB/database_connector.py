import psycopg2


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

