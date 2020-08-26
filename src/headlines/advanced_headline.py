import re, spacy
from collections import namedtuple
from typing import List
from datetime import datetime
from headlines import article_headline
from headlines import search_psql
from commit_DB import database_connector
from commit_DB import webscraper
from commit_DB import create_link


"""
TRANSITIONING CODE FROM USING MORE EXPLICIT CHECKS TO RELYING MORE ON spaCy MODULE. IS NOT FUNCTIONAL OR EVEN LOGICAL YET
"""

class WordAdded(Exception):
    """to break flow of parsing of words when word has been resolved"""
    pass

class NameNotFound(Exception):
    """to break flow of parsing of words when word cannot be located"""
    pass

ProperNoun = namedtuple('ProperNoun', 'noun label') # basically a small container class
Place = namedtuple('Place', 'id name')
Person = namedtuple('Person', 'id name') # name is of type name


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
        proper_nouns: List[ProperNoun] = self.get_all_proper()
        for candidate in proper_nouns:
            try:
                if self.num_words(candidate.noun) == 1:
                    self.parse_single_word(candidate)
                else:
                    self.parse_long_phrase(candidate)
            except NameNotFound or WordAdded:
                continue

    def get_all_proper(self) -> List[ProperNoun]:
        """ Get list of all proper nouns using spaCy"""
        nl_processor = spacy.load("en_core_web_sm")
        analyzed_title = nl_processor(self.title)
        return [ProperNoun(ent.text_, ent.label_) for ent in analyzed_title.ents]

    def num_words(self, phrase) -> int:
        return len(phrase.split(' '))

    def parse_single_word(self, candidate: ProperNoun) -> None:
        """ Parses a single word and if it finds a hit, notes it in the db, etc"""
        found_place: Place = self.search_singleplace(candidate.noun) # will be none if is not place
        if found_place:
            self.note_place(found_place.id, found_place.name)
            return
        if self.search_singlename(candidate):
            return
        if self.search_singleorg(candidate):
            return

    def search_singleplace(self, candidate_place: str):
        """ Checks single word Noun for match to place"""
        place_query = f"Select * from places where pname = '{candidate_place}'"
        search_result = search_psql.query_single(self.connection, place_query)
        try: # checks if there are any results
            return Place(search_result['id'], candidate_place)
        except KeyError:
            return None

    def search_singlename(self, candidate_person: str):
        person_query = f"Select * from famousPeople where last_name = '{candidate_name}'"
        search_person = search_psql.query_single(self.connection, person_query)
        try: # checks if there are any results
            return Person(search_person['id'], Name(search_person['first_name'], search_person['last_name']))
        except KeyError:
            scraped_name = self.scrape_name(candidate_person)
            if scraped_name:
                return Person()

    def scrape_name(self, name) -> Name:
        """ Scrapes a given last name off the web to find the first name"""
        full_name = webscraper.get_full_name(name)
        if full_name:
            name_corrected = full_name.replace('_', ' ')
            split_name = name_corrected.split(' ')
            return Name(split_name[0], split_name[1:].join(''))
        else:
            return None


    def note_place(self, place_id: int, place_name: str):
        create_link.link_headline_place(self.id, place_id)
        self.places.append(place_name)

    def parse_long_phrase(self, candidate)-> None:
        if (self.is_place(candidate)):
            self.add_place(candidate.join(' '))

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



