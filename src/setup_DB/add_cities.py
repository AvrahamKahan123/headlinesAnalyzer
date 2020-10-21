import csv
from headlines.psql_util import get_db_connection
from headlines.psql_util import get_highest_pNoun_id
from typing import List

"""
data taken with permission from https://simplemaps.com/data/world-cities
"""


def get_cities() -> List[str]:
    with open("../../data/worldcities.csv", newline = "") as cities_file:
        city_reader = csv.reader(cities_file, delimiter=",")
        cities = [city_descr[0] for city_descr in city_reader]
        return cities[1:] # skip description line


if __name__ == '__main__':
    connection = get_db_connection()
    cursor = connection.cursor()
    major_cities = get_cities()
    current_id = get_highest_pNoun_id() + 1  # used for assigning serial ids. not really ideal, but is part of setup so is acceptable
    for major_city in major_cities:
        cursor.execute(
            f"INSERT into properNouns(id, fullName, type) values({current_id}, '{major_city}', 'PLACE') ;")
        current_id += 1
    connection.commit()
    connection.close()
