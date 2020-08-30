from headlines.psql_util import get_db_connection

""" File is to be run once to add companies to organizations table"""
if __name__ == '__main__':
    connection = get_db_connection()
    cursor = connection.cursor()
    with open("../../data/companies.txt") as companies:
        for line in companies:
            line = line.replace("\'", "\'\'")
            first_word = line.split(' ')[0]
            if len(first_word) > 2:
                cursor.execute(f"INSERT INTO Organizations(orgName, shortName) Values('{line.strip()}', '{first_word}') on conflict do nothing")

            else:
                cursor.execute(f"INSERT INTO Organizations(orgName) Values('{line.strip()}') on conflict do nothing")
        connection.commit()
