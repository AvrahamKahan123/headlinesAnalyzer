import csv
#THIS FILE WILL ONLY BE RUN ONCE TO SET UP THE FAMOUS PERSON POSTGTGRES DB

import sys
sys.path.insert(1, "../") # allows use of files in src directory above this directory. Acceptable practice since this script will only be run once
import database_connector


# data taken from https://github.com/unitedstates/congress-legislators
def get_congresspeople():
    with open("/home/avraham/PycharmProjects/HeadlinesGrabber/data/congresspeople.csv", newline = "") as cp:
        cong_reader = csv.reader(cp, delimiter = ",")
        congress_people = [(cong[0], cong[1]) for cong in cong_reader]
    return congress_people


if __name__ == '__main__':
    connection = database_connector.get_db_connection()
    cursor = connection.cursor()
    congress_people = get_congresspeople()
    for congress_person in congress_people:
        cursor.execute(f"INSERT into famousPeople(level, lastName, firstName, description) values(3, '{congress_person[0]}', '{congress_person[1]}', 'US Congressperson') ;"
)
    connection.commit()
    connection.close()