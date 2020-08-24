from commit_DB import database_connector

def add_first_names(cursor, connection):
    i=0
    with open("../../data/first_names.txt") as first_names:
        for name in first_names:
            i+=1
            cursor.execute(
                f"INSERT into firstNames(Name, ranking) values('{name.upper()}', {i}) ;"
            )
        connection.commit()


def add_last_names(cursor, connection):
    i=0
    with open("../../data/last_names.txt") as last_names:
        for name in last_names:
            i+=1
            cursor.execute(
                f"INSERT into lastNames(Name, ranking) values('{name}', {i}) ;"
            )
        connection.commit()

if __name__ == '__main__':
    connection = database_connector.get_db_connection()
    cursor = connection.cursor()
    add_first_names(cursor, connection)
    add_last_names(cursor, connection)

