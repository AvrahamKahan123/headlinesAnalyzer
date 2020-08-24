from commit_DB import database_connector


def word_frequency(word: str, cursor):
    word = word.upper()
    sql_query = f"SELECT count(*) FROM allheadlines where upper(title) like '%{word}%'"
    cursor.execute(sql_query)
    count = cursor.fetchone()
    return count[0]

def get_frequencies(words: list) -> int:
    word_frequencies = {}
    connection = database_connector.get_db_connection()
    with connection:
        with connection.cursor() as cursor:
            for word in words:
                word_frequencies[word] = word_frequency(word, cursor)
    connection.close()
    return word_frequencies

#def dated_word_frequency(word: str, )


print(get_frequencies(["Trump", "Biden"]))

