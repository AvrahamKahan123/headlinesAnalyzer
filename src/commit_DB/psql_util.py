

def execute_insert(insert_stmt: str, connection):
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

