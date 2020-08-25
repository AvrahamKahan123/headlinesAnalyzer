import re
from typing import List
from datetime import datetime
from headlines import article_headline
from commit_DB import database_connector
from commit_DB import webscraper
from commit_DB import add_famous


class WordAdded(Exception): # to break flow of parsing of words when word has been resolved
    pass

class NameNotFound(Exception): # if name cannot be located
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

    def __init___(self, title: str, source: str, article_date = datetime.date(datetime.now()), article_time = datetime.time(datetime.now())):
        super().__init__(title, source)
        self.connection = database_connector.get_db_connection()

    def extract_proper_nouns(self) -> None:
        words = self.title.split(" ")
        possible_nouns = self.combine_names([word for word in words])
        for candidate in possible_nouns:
            try:
                if candidate[0][-1] == ".": # is title, ex. Prof., Dr., etc
                    candidate = self.parse_titled(candidate)
                if len(candidate) == 1:
                    if(self.is_place(candidate)):
                        self.add_place(candidate)
                    elif (self.is_last_name(candidate)):
                        full_name = resolve_last_name(candidate)
                        self.add_person(full_name[0], full_name[1])
                    continue

                else:
            except NameNotFound or WordAdded:
                continue

    def is_last_name(self, name):



    def parse_person(self, candidate: List[str], description: str) -> None:
        if len(candidate) == 1:
            name = self.resolve_last_name(candidate[0], description)
            self.add_person(name)
        elif len(candidate) == 2:
            self.add_person(candidate[1], candidate[0])
        else:
            self.add_person(candidate[1:].join(' '), candidate[0])


    def resolve_last_name(self, name, keyword = ""):
        try:
            full_name: Name = self.check_db_lastname(name, keyword)
            return full_name
        except KeyError: # person was not in DB
            pass
        try:
            full_name = self.scrape_name(name)
            return full_name
        except RuntimeError:
            raise NameNotFound



    def scrape_name(self, name):
        full_name = webscraper.get_full_name(name)
        name_split = full_name.split(' ')
        ret = Name(first_name=name_split[0], last_name=name_split[1:].join(' '))
        add_famous.add_famous(ret, 2, "", self.connection)
        return ret

    def check_db_lastname(self, name, keyword) -> Name:
        cursor = self.connection.cursor()
        if keyword == "":
            query = f"SELECT * FROM famousPeople where lastName = {name} and level = 1"
        else:
            query = f"SELECT * FROM famousPeople where lastName = {name} and (level = 1 or Description like '%{keyword}%'"
        fetched = cursor.execute(query)
        return Name(fetched['first_name'], fetched['last_name'])



    def is_place(self, candidate) -> bool:
        cursor = self.connection.cursor()
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

