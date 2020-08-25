from headlines.advanced_headline import Name


def add_famous(n: Name, level: int, description: str, connection) -> None:
    """ Adds a name to the famousPeople PostgreSQL table"""
    cursor = connection.cursor()
    insert_query = f"insert into famousPeople(level, lastName, firstName, Description) values({level}, {n.last_name}, {n.first_name}, '{description}'"
    cursor.execute(insert_query)
    connection.commit()


