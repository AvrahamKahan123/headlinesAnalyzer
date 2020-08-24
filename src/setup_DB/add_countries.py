
import sys
sys.path.insert(1, "../") # allows use of files in src directory above this directory. Acceptable practice since this script will only be run once
import database_connector



if __name__ == '__main__':
    connection = database_connector.get_db_connection()
    cursor = connection.cursor()
    with open("../../data/countries.txt") as country_file: # source https://textlists.info/geography/countries-of-the-world/
        countries = country_file.readlines()
    for country in countries:
        cursor.execute( f"INSERT into places(id, cname) values(-1, '{country.strip()}') ;" )
    connection.commit()
    connection.close()
