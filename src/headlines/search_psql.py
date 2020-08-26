

def query_single(connection, query):
    cursor = connection.cursor()
    cursor.execute(query)
    return cursor.fetchone()