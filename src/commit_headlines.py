import psycopg2

def connect_to_database():
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


def closeDatabase(connection, cursor):
    cursor.close()
    connection.close()

def addHeadlinesToDB(headlineConnection, cursor):
    additions = []
    fox_Headlines = get_fox_headlines()
    additions.extend(createAddQuery(fox_Headlines, "fox"))
    msnbc_Headlines = get_MSNBC_headlines()
    additions.extend(createAddQuery(msnbc_headlines, "msnbc"))
    abc_Headlines = get_ABC_headlines()
    additions.extend(createAddQuery(abc_Headlines, "abc"))
    for addQuery in additions:
        cursor.execute(addQuery)
    headlineConnection.commit()

def createAddQuery(headlines: list, source, )  -> list:
    ret = []
    for headline in headlines:
        ret.append(f"INSERT INTO TABLE allHeadlines( newsOrg, title, articleDate, articleTime) values ({source}, CURRENT_TIME, CURRENT_DATE)")
    return ret




