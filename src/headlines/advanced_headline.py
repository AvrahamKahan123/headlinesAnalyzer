import re
from typing import List
from headlines import article_headline
from commit_DB import database_connector
from commit_DB import webscraper


class WordAdded(Exception): # to break flow of parsing of words when word has been resolved
    pass

class Name():
    def __init__(self, first_name = "", last_name = ""):
        self.first_name = first_name
        self.last_name = last_name
    def set_full_name(self, name : str):
        split_up_name = name.split(' ')
        self.first_name = split_up_name[0]
        self.last_name = split_up_name[1:].join(' ')


class AdvancedHeadline(article_headline.ArticleHeadline):


    def extract_proper_nouns(self) -> None:
        connection = database_connector.get_db_connection()
        cursor = connection.cursor()
        words = self.title.split(" ")
        possible_nouns = self.combine_names([word for word in words])
        for candidate in possible_nouns:
            try:
                if candidate[0][-1] == ".": # is title, ex. Prof., Dr., etc
                    candidate = self.parse_titled(candidate, connection)
                if len(candidate) == 1:
                    if(is_place(candidate, connection)):
                        self.add_place(candidate)
                    elif (is_last_name(candidate)):
                        full_name = resolve_last_name(candidate)
                        self.add_person(full_name[0], full_name[1])
                    continue

                else:
            except:
                continue

    def parse_person(self, candidate: List[str], connection, description: str) -> None:
        if len(candidate) == 1:
            name = resolve_last_name(candidate[0], description)
            self.add_person(name)
        elif len(candidate) == 2:
            self.add_person(candidate[1], candidate[0])
        else:
            self.add_person(candidate[1:].join(' '), candidate[0])


    def resolve_last_name(self, name, connection, keyword = ""):
        try:
            full_name: Name = self.check_db_lastname(name, connection, keyword)
        except KeyError: # person was not in DB
            pass
        try:
            name = self.scrape_name(name, connection)


    def scrape_name(self, name):
        full_name = webscraper.get_full_name(name)




    def check_db_lastname(self, name, connection, keyword) -> Name:
        cursor = connection.cursor()
        if keyword == "":
            query = f"SELECT * FROM famousPeople where lastName = {name} and level = 1"
        else:
            query = f"SELECT * FROM famousPeople where lastName = {name} and (level = 1 or Description like '%{keyword}%'"
        fetched = cursor.execute(query)
        return Name(fetched['first_name'], fetched['last_name'])



    def is_place(self, candidate, connection) -> bool:
        cursor = connection.cursor()
        place_query = f"Select count(*) from places where cname = '{candidate}'"
        cursor.execute(place_query)
        number = cursor.fetchone()
        return number['count'] > 0


    def parse_titled(self, candidate) -> List[str]:
        if candidate[0] == "Sen." or candidate[0] == "Rep.":
            self.parse_person(candidate[1:], "congress")
            raise WordAdded
        elif candidate[0] == "Pres.":
            self.add_person("Trump", "Donald")
            raise WordAdded
        else:
            return candidate[1:]



    def combine_names(self, possible_names) -> List[str]:
        filtered_names = []
        current_name = []
        for name in possible_names:
            if name[0].islower():
                if (len(current_name) > 0):
                    filtered_names.append([current_name])
            elif bool(re.match(name[-1], ",|'|:|;")) or (name[-2] == "'" and name[-1] == "s"):
                current_name.append(name)
                filtered_names.append(current_name)
                current_name = ""
            elif name[0].islower():
                if (len(current_name) > 0):
                    filtered_names.append(current_name)
                current_name = ""
            else:
                current_name.append(name)
        return filtered_names

