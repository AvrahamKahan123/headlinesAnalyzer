import re, spacy
from typing import List
from datetime import datetime
from headlines import article_headline
from commit_DB import database_connector
from commit_DB import webscraper
from commit_DB import add_famous


class WordAdded(Exception):
    """to break flow of parsing of words when word has been resolved"""
    pass

class NameNotFound(Exception):
    """to break flow of parsing of words when word cannot be located"""
    pass


class Name():
    """ Wrapper to hold name of a person"""
    def __init__(self, first_name = "", last_name = ""):
        self.first_name = first_name
        self.last_name = last_name
    def set_full_name(self, name : str):
        split_up_name = name.split(' ')
        self.first_name = split_up_name[0]
        self.last_name = split_up_name[1:].join(' ')


class AdvancedHeadline(article_headline.ArticleHeadline):
    """ Provides functionality to discover names, places, and other proper nouns mentioned in headlines"""

    def __init___(self, title: str, source: str, article_date = datetime.date(datetime.now()), article_time = datetime.time(datetime.now())):
        super().__init__(title, source)
        self.connection = database_connector.get_db_connection()

    def extract_proper_nouns(self) -> None:
        """ Extacts names, places, etc. and stores them to the places variable """
        words = self.title.split(" ")
        possible_nouns = self.get_all_proper()
        for candidate in possible_nouns:
            try:
                if candidate[0][-1] == ".": # is title, ex. Prof., Dr., etc
                    candidate = self.parse_titled(candidate)
                if len(candidate) == 1:
                    self.parse_single_word(candidate)
                    continue
                else:
                    self.parse_long_phrase(candidate)

            except NameNotFound or WordAdded:
                continue

    def get_all_proper(self):
        nlp = spacy.load("en_core_web_sm")
        title_doc = nlp(self.title)
        all_nouns = []
        for token in title_doc:
            if token.pos_ == "PROPN":
                all_nouns.append(token.text_.split(' '))
        return all_nouns



    def parse_long_phrase(self, candidate):
        if (self.is_place(candidate.join(' '))):
            self.add_place(candidate.join(' '))

    def parse_single_word(self, candidate):
        if (self.is_place(candidate)):
            self.add_place(candidate)
        elif (self.is_last_name(candidate)):
            full_name = self.resolve_last_name(candidate)
            self.add_person(full_name[0], full_name[1])
        elif


    def combine_names(self, possible_names) -> List[str]:
        """ Combines consecutive capitalized words into names and proper nouns"""
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

    def is_last_name(self, name) -> bool:
        """ :return if given name is a last name"""
        cursor = self.connection.cursor()
        query = f"Select count(*) from lastNames where name = '{name}'"
        cursor.execute()
        return cursor.fetchone()['count'] > 0

    def parse_person(self, candidate: List[str], description: str) -> None:
        """ Parses given name to try to identify the person"""
        if len(candidate) == 1:
            name = self.resolve_last_name(candidate[0], description)
            self.add_person(name)
        elif len(candidate) == 2:
            self.add_person(candidate[1], candidate[0])
        else:
            self.add_person(candidate[1:].join(' '), candidate[0])

    def resolve_last_name(self, name, keyword = ""):
        """ Given a last name, tries to find the full name"""
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
        """ Scrapes a given last name off the web to find the first name"""
        full_name = webscraper.get_full_name(name)
        name_split = full_name.split(' ')
        ret = Name(first_name=name_split[0], last_name=name_split[1:].join(' '))
        add_famous.add_famous(ret, 2, "", self.connection)
        return ret

    def check_db_lastname(self, name, keyword) -> Name:
        """ :return Name object with given name from DB"""
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
        """ Parses a person who has a title, ex. Dr."""
        if candidate[0] == "Sen." or candidate[0] == "Rep.":
            self.parse_person(candidate[1:], "congress")
            raise WordAdded
        elif candidate[0] == "Pres.":
            self.add_person("Trump", "Donald")
            raise WordAdded
        else:
            return candidate[1:]



