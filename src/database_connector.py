import psycopg2

def get_db_connection():
    try:
        # WOULD BE MAJOR SECURITY HOLE IF WAS CONNECTABLE TO FROM OUTSIDE SINCE PASSWORD IS WRITTEN HERE
        headlineConnection = psycopg2.connect(user = "adminheadlines",
                                      password = "abc123",
                                      host = "127.0.0.1",
                                      port = "5432",
                                      database = "headlines")
        return headlineConnection
    except (Exception, psycopg2.Error) as error :
        print ("Error when attempting to connect to Headlines database", error)
