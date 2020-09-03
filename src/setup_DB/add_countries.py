from headlines.psql_util import get_db_connection
from headlines.psql_util import get_highest_pNoun_id

""" RUN ONCE"""
if __name__ == '__main__':
    connection = get_db_connection()
    cursor = connection.cursor()
    current_id = get_highest_pNoun_id() + 1
    with open("../../data/countries.txt") as country_file: # source https://textlists.info/geography/countries-of-the-world/
        countries = country_file.readlines()
    for country in countries:
        cursor.execute( f"INSERT into properNouns(id, fullName, type) values({current_id}, '{country.strip()}', 'PLACE') ;" )
        current_id +=1
    connection.commit()
    connection.close()
