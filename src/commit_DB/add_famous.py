from headlines.advanced_headline import Name
from commit_DB.create_link import execute_insert


def add_famous(n: Name, level: int, description: str, connection) -> int:
    """ Adds a name to the famousPeople PostgreSQL table"""
    insert_query = f"insert into famousPeople(level, lastName, firstName, Description) values({level}, {n.last_name}, {n.first_name}, '{description}'"
    execute_insert(insert_query)



