from commit_headlinesDB import database_connector
from typing import Dict


def word_frequency(word: str, cursor) -> int:
    """ Gets word frequency in headlines for a given word"""
    word = word.upper()
    sql_query = f"SELECT count(*) FROM allheadlines where upper(title) like '%{word}%'"
    cursor.execute(sql_query)
    count = cursor.fetchone()
    return count[0]


def get_frequencies(words: list) -> Dict[str, int]:
    """ Gets word frequencies in headlines for a list of words"""
    word_frequencies = {}
    connection = database_connector.get_db_connection()
    with connection:
        with connection.cursor() as cursor:
            for word in words:
                word_frequencies[word] = word_frequency(word, cursor)
    connection.close()
    return word_frequencies


print(get_frequencies(["Trump", "Biden"]))

