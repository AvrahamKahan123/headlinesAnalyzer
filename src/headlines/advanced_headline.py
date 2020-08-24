import re
from headlines import article_headline
from commit_DB import database_connector


class WordAdded(Exception): # to break flow of parsing of words when word is already added
    pass

class AdvancedHeadline(article_headline.ArticleHeadline):


    def extract_proper_nouns(self):
        connection = database_connector.get_db_connection()
        cursor = connection.cursor()
        words = self.title.split(" ")
        possible_nouns = self.combine_names([word for word in words])
        for candidate in possible_nouns:
            candidate = candidate.split(' ')
            try:
                if candidate[0][-1] == ".": # is title, ex. Prof., Dr., etc
                    candidate = self.parse_titled(candidate, cursor, connection)
                if len(candidate) == 1:
                    if(is_place(candidate)):
                        self.add_place(candidate)
                    elif (is_last_name(candidate)):
                        full_name = resolve_last_name(candidate)
                        self.add_person(full_name[0], full_name[1])
                    continue

                else:
            except:
                continue

    def is_place(self, candidate, cursor):
        place_query = f"Select count(*) from places where cname = '{candidate}'"
        cursor.execute(place_query)
        number = cursor.fetchone()
        return number['count'] > 0

    def parse_titled(self, candidate, cursor, connection):
        if candidate[0] == "Sen." or candidate[0] == "Rep.":
            add_congressperson(candidate, cursor, connection)
            raise WordAdded
        elif candidate[0] == "Pres.":
            self.add_person("Trump", "Donald")
            raise WordAdded
        else:
            return candidate[1:]


    def combine_names(self, possible_names):
        filtered_names = []
        current_name = ""
        for name in possible_names:
            if name[0].islower():
                if (len(current_name) > 0):
                    filtered_names.append(current_name)
            elif bool(re.match(name[0], ",|'|:|;")) or (name[-2] == "'" and name[-1] == "s"):
                current_name += name
                filtered_names.append(current_name)
                current_name = ""
            elif name[0].islower():
                if (len(current_name) > 0)
                    filtered_names.append(current_name)
                current_name = ""
            else:
                current_name+=name
        return filtered_names



