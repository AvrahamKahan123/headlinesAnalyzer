from headlines.psql_util import get_db_connection
from headlines.psql_util import query_single_field

""" File is to be run once to add companies to organizations table"""
if __name__ == '__main__':
    connection = get_db_connection()
    cursor = connection.cursor()
    query_highest = f"SELECT MAX(ID) from ProperNouns"
    id = query_single_field(query_highest, connection) + 1
    with open("../../data/companies.txt") as companies:
        for line in companies:
            line = line.replace("\'", "\'\'")
            first_word = line.split(' ')[0]
            if len(first_word) > 2:
                cursor.execute(f"INSERT INTO ProperNouns(id, fullName) Values({id}, '{line.strip()}') on conflict do nothing")
                cursor.execute(f"INSERT INTO Nicknames(id, nickname) Values({id}, '{line.strip.split(' ')[0]}'")
            else:
                cursor.execute(f"INSERT INTO ProperNouns(id, fullName) Values({id}, '{line.strip()}') on conflict do nothing")
            id+=1
        connection.commit()
