from commit_DB import database_connector

if __name__ == '__main__':
    connection = database_connector.get_db_connection()
    cursor = connection.cursor()
    with open("../../data/countries.txt") as country_file: # source https://textlists.info/geography/countries-of-the-world/
        countries = country_file.readlines()
    for country in countries:
        cursor.execute( f"INSERT into places(pname) values('{country.strip()}') ;" )
    connection.commit()
    connection.close()
