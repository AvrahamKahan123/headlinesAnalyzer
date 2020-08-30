import spacy, json
from collections import namedtuple
from typing import List
from datetime import datetime
from nltk.tokenize import WhitespaceTokenizer
from nltk.stem.snowball import SnowballStemmer
from headlines import webscraper
from headlines import psql_util


"""
TRANSITIONING CODE FROM USING MORE EXPLICIT CHECKS TO RELYING MORE ON spaCy MODULE. IS NOT FUNCTIONAL OR EVEN LOGICAL YET

PARSING of titles IS NOT FUNCTIONAL YET
"""


class ArticleHeadline:
    """ Represents headline parsed from web. Contains id of Article in postgres, as well as extracted peoples, places, and organizations"""
    def __init__(self, title: str, source: str, article_date = datetime.date(datetime.now()), article_time = datetime.time(datetime.now()), id = -1,
                 people = [], places = [], proper_nouns = []):
        self.title = title.replace("\'", "\'\'")
        self.source = source
        self.article_date = article_date
        self.article_time = article_time
        self.people = people
        self.places = places
        self.proper_nouns = proper_nouns
        self.id = id
        self.topic_index = -1

    def tokenized(self) -> List[str]:
        """ Extracts stemmed and cleaned tokens of title. May be used as part of the parsing"""
        tokens = self.tokenizer(self.title)
        cleaned_tokens = self.remove_stop_words(tokens)
        stemmed_tokens = self.stemmer(cleaned_tokens)
        return stemmed_tokens

    def tokenizer(self, text):
        """ Tokenize title"""
        tokenizer = WhitespaceTokenizer()
        tokenized_list = tokenizer.tokenize(self.title)
        return tokenized_list

    def remove_stop_words(self, tokens):
        stopwords = spacy.lang.en.stop_words.STOP_WORDS
        cleaned_tokens = filter(lambda x: x not in stopwords, tokens)
        return cleaned_tokens

    def stemmer(tokens: List[str]):
        """ Stem tokenized title"""
        snowball = SnowballStemmer(language='english')
        stemmed_list = [snowball.stem(word) for word in tokens]
        return stemmed_list

    def get_all_pnouns(self):
        """ Returns list containing all proper nouns for this headline"""
        return self.places + self.people + self.orgs + self.proper_nouns

    def add_person(self, first_name, last_name):
        self.people.append(first_name + " " + last_name)

    def add_place(self, place):
        self.places.append(place)

    def add_pnoun(self, p_noun):
        self.proper_nouns.append(p_noun)

    def cleaned(self):
        return self.tokenized().join(' ')

    def __str__(self):
        return self.title

    def to_json(self):
        data_dict = {"title": self.title, "source": self.source, "atime": self.article_time, "adate": self.article_date, "apeople": self.people}
        return json.dumps(data_dict)

    def create_insert(self) -> str:
        """ Returns insert statement for article """
        return f"INSERT into allheadlines(newsorg, title, articledate, articletime) values('{self.source}', '{self.title}', CURRENT_DATE, CURRENT_TIME) ON CONFLICT DO NOTHING;"


ProperNoun = namedtuple('ProperNoun', 'noun label') # basically a small container class with fields noun and label
Place = namedtuple('Place', 'id name')
Person = namedtuple('Person', 'id name') # name is of type name
Organization = namedtuple('Organization', 'id name')
Name = namedtuple('Name', 'first_name last_name')


class HeadlineParser():
    """ Provides functionality to discover names, places, and other proper nouns mentioned in headline """
    def __init___(self, headline: ArticleHeadline):
        self.headline = headline
        self.connection = psql_util.get_db_connection()

    def extract_proper_nouns(self) -> None:
        """ Extacts names, places, etc. and stores them to the places variable """
        proper_nouns: List[ProperNoun] = self.get_all_proper()
        for candidate in proper_nouns:
            if self.num_words(candidate.noun) == 1:
                self.parse_single_word(candidate)
            else:
                self.parse_long_phrase(candidate)

    def num_words(self, phrase) -> int:
        return len(phrase.split(' '))

    def get_all_proper(self) -> List[ProperNoun]:
        """ Get list of all proper nouns using spaCy"""
        nl_processor = spacy.load("en_core_web_sm")
        analyzed_title = nl_processor(self.title)
        return [ProperNoun(ent.text_, ent.label_) for ent in analyzed_title.ents] # ent returns only entities (ie. proper nouns)

    def parse_single_word(self, candidate: ProperNoun) -> None:
        """ Parses a single word and if it finds a hit, notes it in the db, etc
        Code must be added to remove punctuation and if need be, lemmatize the word"""
        if candidate.label == "NORP": # some kind of group, ex. 'Israeli'
            pass
            # code to strip off tailing text (ex. the -ian in 'Floridian'). Another function will be made to support fuzzier matching for places
        found_place: Place = self.search_singleplace(candidate.noun) # will be none if is not place
        if found_place:
            self.note_place(found_place.id, found_place.name)
            return
        found_name: Person = self.search_singlename(candidate)
        if found_name:
            self.note_name(found_name.id, found_name.name)
            return
        found_org = self.search_singleorg(candidate)
        if found_org:
            self.note_org(found_org)
            return
        self.headline.add_pnoun(candidate)

    def search_singleplace(self, candidate_place: str) -> Place:
        """ Checks single word Noun for match to place"""
        place_query = f"Select * from places where pname = '{candidate_place}'"
        search_result = (self.connection, place_query)
        if search_result is None: # checks if there are any results
            return Place(search_result['id'], candidate_place)
        # will return none if search_result = None

    def note_place(self, place_id: int, place_name: str):
        psql_util.link_headline_place(self.id, place_id)
        self.headline.add_place(place_name)

    def search_singlename(self, candidate_person: str) -> Person:
        person_query = f"Select * from famousPeople where last_name = '{candidate_person}'"
        search_person = psql_util.query_full_row(person_query, self.connection)
        try: # checks if there are any results
            return Person(search_person['id'], Name(search_person['first_name'], search_person['last_name']))
        except TypeError:
            scraped_name = self.scrape_name(candidate_person)
            if scraped_name:
                psql_util.add_famous(scraped_name, 2, "", self.connection)
                newperson_Id = psql_util.query_single_field(f"SELECT id FROM famousPeople WHERE lastName = {scraped_name.last_name} and firstName = {scraped_name.first_name}")
                return Person(newperson_Id, scraped_name)
            else:
                return None

    def scrape_name(self, name) -> Name:
        """ Scrapes a given last name off the web to find the first name"""
        full_name = webscraper.get_full_name(name)
        if full_name:
            name_corrected = full_name.replace('_', ' ')
            split_name = name_corrected.split(' ')
            return Name(split_name[0], split_name[1:].join(''))
        else:
            return None

    def note_name(self, linked_person: Person):
        psql_util.link_headline_person(self.id, linked_person.id)
        self.headline.add_person(linked_person.name.first_name + " " + linked_person.name.last_name)


    def search_singleorg(self, candidate):
        """ Will search organizations table for possible match to candidate"""
        pass

    def parse_long_phrase(self, candidate)-> None:
        """ Incomplete. Will parse and lemmatize the candidate and then search against databases"""
        if (self.is_place(candidate)):
            self.add_place(candidate.join(' '))


    def parse_person(self, candidate: List[str], description: str) -> None:
        """ Parses given name to try to identify the person"""
        if len(candidate) == 1:
            name = self.resolve_last_name(candidate[0], description)
            self.add_person(name)
        elif len(candidate) == 2:
            self.add_person(candidate[1], candidate[0])
        else:
            self.add_person(candidate[1:].join(' '), candidate[0])

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

    def is_last_name(self, name) -> bool:
        """ :return if given name is a last name"""
        cursor = self.connection.cursor()
        query = f"Select count(*) from lastNames where name = '{name}'"
        cursor.execute()
        return cursor.fetchone()['count'] > 0


