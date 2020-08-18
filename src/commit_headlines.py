import psycopg2
import webscraper

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


def close_db(connection, cursor):
    cursor.close()
    connection.close()

def addHeadlinesToDB(headlineConnection, cursor):
    additions = []
    fox_Headlines = webscraper.get_fox_headlines()
    additions.extend(createInsertStatements(fox_Headlines, "fox"))
    msnbc_Headlines = webscraper.get_MSNBC_headlines()
    print(msnbc_Headlines)
    additions.extend(createInsertStatements(msnbc_Headlines, "msnbc"))
    abc_Headlines = webscraper.get_ABC_headlines()
    additions.extend(createInsertStatements(abc_Headlines, "abc"))
    for addQuery in additions:
        cursor.execute(addQuery)
    headlineConnection.commit()

def createInsertStatements(headlines: list, source, )  -> list:
    ret = []
    for headline in headlines:
        headline = headline.replace("\'", "\'\'")
        ret.append(f"INSERT into allheadlines(newsorg, title, articledate, articletime) values('{source}', '{headline}', CURRENT_DATE, CURRENT_TIME) ;")
    return ret


def update_DB():
    connection = get_db_connection()
    cursor = connection.cursor()
    addHeadlinesToDB(connection, cursor)
    close_db(connection, cursor)
