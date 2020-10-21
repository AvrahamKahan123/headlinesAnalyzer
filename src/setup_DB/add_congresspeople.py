import csv
from headlines.psql_util import get_db_connection
from headlines.psql_util import get_highest_pNoun_id

#THIS FILE WILL ONLY BE RUN ONCE TO SET UP PART OF THE ProperNOUN table in POSTGTGRES DB

# data taken from https://github.com/unitedstates/congress-legislators
def get_congresspeople():
    with open("/home/avraham/PycharmProjects/HeadlinesGrabber/data/congresspeople.csv", newline = "") as cp:
        cong_reader = csv.reader(cp, delimiter = ",")
        congress_people = [(cong[0], cong[1]) for cong in cong_reader]
    return congress_people


if __name__ == '__main__':
    connection = get_db_connection()
    cursor = connection.cursor()
    congress_people = get_congresspeople()
    current_id= get_highest_pNoun_id() + 1  # used for assigning serial ids. not really ideal, but is part of setup so is acceptable
    for congress_person in congress_people:
        cursor.execute(f"INSERT into properNouns(id, fullName, type) values({current_id}, '{congress_person[0] + congress_person[1]}', 'PERSON') ;")
        current_id+=1
    connection.commit()
    connection.close()
