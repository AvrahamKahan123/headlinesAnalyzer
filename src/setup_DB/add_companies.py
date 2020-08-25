from commit_DB import database_connector

if __name__ == '__main__':
    connection = database_connector.get_db_connection()
    cursor = connection.cursor()
    with open("../../data/companies.txt") as companies:
        for line in companies:
            line = line.replace("\'", "\'\'")
            first_word = line.split(' ')[0]
            if len(first_word) > 2 and first_word.upper() == first_word:
                cursor.execute(f"INSERT INTO Organizations(orgName, abbreviation) Values('{line.strip()}', '{first_word}')")

            else:
                cursor.execute(f"INSERT INTO Organizations(orgName) Values('{line.strip()}')")
        connection.commit() 
