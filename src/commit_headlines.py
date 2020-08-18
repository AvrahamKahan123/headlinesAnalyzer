import webscraper, database_connector


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
    connection = database_connector.get_db_connection()
    with connection:
        with connection.cursor() as cursor:
            addHeadlinesToDB(connection, cursor)
    connection.close()
